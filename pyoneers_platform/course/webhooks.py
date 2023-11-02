"""
The application's database is kept in sync with the repository (https://github.com/ThePyoneerProject/course)
via webhooks. Chapter and Section models are automatically created, updated, or deleted on every push to the repo,
according to the latest content in the repo.

Functions:
    - handle_github_webhook: Authenticates GitHub webhook and triggers content update.
    - sync_with_github: Updates Chapters and Sections from the repo.
"""

import hashlib
import hmac
import os

import git
import markdown2
import yaml
from django.conf import settings
from django.db import transaction
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

from pyoneers_platform.course.models import Chapter, Section


@csrf_exempt
def handle_github_webhook(request: HttpRequest) -> JsonResponse | HttpResponseForbidden:
    """
    Handle incoming GitHub webhooks.

    This function receives GitHub webhook POST requests, validates them,
    and triggers the fetching and parsing of the repository.

    Parameters:
        request (HttpRequest): The incoming HTTP request object from Django.

    Returns:
        JsonResponse: A JSON object with a 'status' field, indicating success.
        HttpResponseForbidden: 403 status code, indicating authentication failure or invalid method.

    Use Case:
        Set this up on your server and configure GitHub to ping this URL
        every time there's a push to your repo. Your Django models get updated
        according to the latest content in the repo.
    """

    def is_valid_signature(request_signature: str, payload: bytes) -> bool:
        """Validate the GitHub signature."""
        secret = settings.GITHUB_SECRET.encode()
        computed_signature = hmac.new(secret, msg=payload, digestmod=hashlib.sha1).hexdigest()
        return hmac.compare_digest(f"sha1={computed_signature}", request_signature)

    signature = request.headers.get("x-hub-signature")

    if signature is None:
        return HttpResponseForbidden("Permission denied. No signature found.")

    if not is_valid_signature(signature, request.body):
        return HttpResponseForbidden("Permission denied. Invalid signature.")

    if request.method == "POST":
        repo_url = "https://github.com/ThePyoneerProject/course"
        try:
            with transaction.atomic():
                sync_with_github(repo_url)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return HttpResponseForbidden(f"Permission denied. {e}")

    return HttpResponseForbidden("Permission denied. Invalid HTTP method.")


def sync_with_github(repo_url: str, local_path: str = "/tmp/repo"):
    """
    Clone or pull a Git repository and update the Django models based on its content.
    Also sets the order and title of Chapters and Sections based on the meta.yaml files and Markdown front matter.

    Parameters:
        repo_url (str): The URL of the Git repository to clone or pull.
        local_path (str): The local directory where the repository will be cloned or pulled.

    Use Case:
        This function keeps the database in sync with the repo.
    """

    # Clone or pull the repository to local storage
    if not os.path.exists(local_path):
        git.Repo.clone_from(repo_url, local_path)
        logger.debug(f"Cloned repository to {local_path}")
    else:
        repo = git.Repo(local_path)
        repo.remotes.origin.pull()
        logger.debug(f"Updated existing repository at {local_path}")

    # List all directory names in the repository, ignoring the .git folder
    chapter_folders = [
        folder_name
        for folder_name in os.listdir(local_path)
        if os.path.isdir(os.path.join(local_path, folder_name)) and folder_name != ".git"
    ]

    # Delete chapters not in the repo
    Chapter.objects.exclude(slug__in=chapter_folders).delete()

    # Iterate over all folders in the repo (which represent chapters)
    for folder_name in chapter_folders:
        # Read chapter's meta information from the meta.yaml file
        meta_file_path = os.path.join(local_path, folder_name, "meta.yaml")
        with open(meta_file_path) as f:
            meta_content = yaml.load(f, Loader=yaml.FullLoader)

        # Create or update chapter based on folder name and meta information
        chapter, _ = Chapter.objects.update_or_create(
            slug=folder_name,
            defaults={
                "title": meta_content.get("title", folder_name.replace("_", " ").title()),
                "order": meta_content.get("order", 0),
            },
        )
        logger.debug(f"Updated chapter {folder_name}")

        # List all markdown files in the directory (i.e., sections)
        section_files = [f for f in os.listdir(os.path.join(local_path, folder_name)) if f.endswith(".md")]

        # Delete sections not in the repo
        chapter.sections.exclude(slug__in=[filename[:-3] for filename in section_files]).delete()

        # Iterate over all markdown files in the folder (which represent sections)
        for file_name in section_files:
            # Read section content from file
            section_file_path = os.path.join(local_path, chapter.slug, file_name)
            with open(section_file_path) as f:
                section_content = f.read()

            # Parse section slug from file name
            slug = file_name.replace(".md", "")

            # Parse Markdown content
            parsed_content = markdown2.markdown(section_content, extras=["metadata"])

            # Parse section order and title from Markdown file's yaml front matter
            parsed_order = int(parsed_content.metadata.get("order", 0))
            parsed_title = parsed_content.metadata.get("title", slug.replace("_", " ").title())

            Section.objects.update_or_create(
                chapter=chapter,
                slug=slug,
                defaults={"content": parsed_content, "order": parsed_order, "title": parsed_title},
            )
            logger.debug(f"Updated section {chapter.slug}/{file_name}")
