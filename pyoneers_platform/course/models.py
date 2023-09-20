import re

from django.shortcuts import redirect
from django.utils.text import slugify
from modelcluster.models import ClusterableModel
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page, Orderable
from wagtailmarkdown.fields import MarkdownField

from pyoneers_platform.course.utils import get_current_module


class Module(Page):
    """
    Module represents a collection of chapters in a course.

    Attributes:
        description: Description of the module in Markdown.
    """

    subpage_types = ["course.Chapter"]

    description = MarkdownField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Add current module to context (for sidebar)
        context["current_module"] = get_current_module(self)

        return context

    def serve(self, request, *args, **kwargs):
        # Get the first chapter under this module
        first_chapter = Chapter.objects.live().child_of(self).first()

        # If a first chapter exists, redirect to it
        if first_chapter:
            return redirect(first_chapter.url)

        # If no first chapter exists, just serve the Module page as usual
        return super().serve(request, *args, **kwargs)


class Chapter(Page):
    """
    Represents a chapter with multiple sections, auto-created from the Markdown `content` field.
    """

    parent_page_types = ["course.Module"]

    icon = models.CharField(max_length=255, blank=True)
    content = MarkdownField(
        blank=True,
        null=True,
        help_text="Use '#' to create sections. "
        "Each section will be turned into a separate page in the course's chapter automatically.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("title"),
        FieldPanel("icon"),
        FieldPanel("content"),
    ]

    @property
    def sections(self):
        """
        Parses the Markdown content into sections and returns a list of them.

        Each section is a dictionary containing:
        - slug: A slugified version of the title.
        - number: The section's page number within the chapter.
        - name: The title of the section.
        - url: The URL to the specific section.
        """
        raw_sections = re.split(r"\n# ", self.content)
        parsed_sections = [raw_sections[0]] + ["# " + section for section in raw_sections[1:]]

        sections_list = []
        total_sections = len(parsed_sections)
        for i, content in enumerate(parsed_sections, 1):
            title = content.split("\n")[0].replace("# ", "")
            slug = slugify(title)
            section = {
                "slug": slug,
                "number": i,
                "name": title,
                "content": content,
                "url": f"{self.url}?page={i}",
                "has_next": i < total_sections,
                "has_previous": i > 1,
                "next_section_url": f"{self.url}?page={i + 1}" if i < total_sections else None,
                "previous_section_url": f"{self.url}?page={i - 1}" if i > 1 else None,
            }
            sections_list.append(section)

        return sections_list

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Add current module to context (for sidebar)
        context["current_module"] = get_current_module(self)

        # Get the current page number from the request
        page_number = int(request.GET.get("page", 1))

        # Find the current section and add it to the context
        section = next((s for s in self.sections if s["number"] == page_number), None)
        if section:
            context["current_section"] = section

        return context
