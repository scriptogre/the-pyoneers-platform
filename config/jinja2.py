import os

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.templatetags.socialaccount import get_adapter
from allauth.utils import get_request_param
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from jinja2 import pass_context
from jinja2.ext import Extension
from markupsafe import Markup


class AllAuthExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals.update(
            {
                "provider_login_url": self.provider_login_url,
                "get_social_accounts": self.get_social_accounts,
                "get_providers": self.get_providers,
            }
        )

    @pass_context
    def provider_login_url(self, context, provider_id, **kwargs):
        request = context.get("request")  # Fetch request from context

        adapter = get_adapter(request)
        provider = adapter.get_provider(request, provider_id)
        query = kwargs
        auth_params = query.get("auth_params", None)
        scope = query.get("scope", None)
        process = query.get("process", None)

        if scope == "":
            del query["scope"]
        if auth_params == "":
            del query["auth_params"]

        if "next" not in query:
            next = get_request_param(request, "next")
            if next:
                query["next"] = next
            elif process == "redirect":
                query["next"] = request.get_full_path()
        else:
            if not query["next"]:
                del query["next"]

        return provider.get_login_url(request, **query)

    def get_social_accounts(self, user):
        return SocialAccount.objects.filter(user=user)

    def get_providers(self):
        return providers.registry.get_class_list()


def svg(filename, css_classes=None):
    """
    Retrieve an SVG file from the specified path and optionally add a CSS class to it.

    Parameters:
    filename (str): The name of the SVG file without the file extension.
    css_classes (str, optional): A CSS class to add to the SVG. Defaults to None.

    Returns:
    jinja2.Markup: The SVG content marked as safe HTML, or an empty string if the file is not found.

    Raises:
    Exception: If the SVG file is not found and settings.DEBUG is True.
    """

    path = finders.find(os.path.join("svg", f"{filename}.svg"), all=True)

    if not path:
        message = f"SVG '{filename}.svg' not found"

        # Raise exception if DEBUG is True
        if settings.DEBUG:
            raise Exception(message)  # Exception name adjusted
        else:
            return ""

    # Sometimes path can be a list/tuple if there's more than one file found
    if isinstance(path, (list, tuple)):
        path = path[0]

    with open(path) as svg_file:
        svg_content = svg_file.read()

    if css_classes:
        soup = BeautifulSoup(svg_content, "html.parser")
        svg_tag = soup.find("svg")
        if svg_tag:
            existing_classes = svg_tag.get("class", [])
            # Ensure existing_classes is a list
            if not isinstance(existing_classes, list):
                existing_classes = [existing_classes]
            # Append the new class
            existing_classes.append(css_classes)
            svg_tag["class"] = " ".join(existing_classes)
            svg_content = str(soup)

    return Markup(svg_content)


def avatar_url(user):
    if user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=user).first()
        if social_account:
            return social_account.get_avatar_url()
    return static("img/avatar-default.webp")
