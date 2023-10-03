import re

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtailmarkdown.fields import MarkdownField


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

    @property
    def chapters(self):
        # Fetch all live child Chapter objects under this Module
        return Chapter.objects.live().child_of(self).order_by("id")

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
    chapter_content = MarkdownField(
        blank=True,
        null=True,
        help_text=(
            "Use '#' to create sections. "
            "Each section will be turned into a separate Section object automatically. "
            "DO NOT create or modify Section objects manually."
        ),
    )

    content_panels = Page.content_panels + [
        FieldPanel("icon"),
        FieldPanel("chapter_content"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Paginate sections
        paginator = Paginator(self.sections.all().order_by("order"), 1)

        # Get the current section
        current_page = request.GET.get("page", 1)
        try:
            paginated_sections = paginator.page(current_page)
        except PageNotAnInteger:
            paginated_sections = paginator.page(1)
        except EmptyPage:
            paginated_sections = paginator.page(paginator.num_pages)
        if paginated_sections:
            current_section = paginated_sections[0]
        else:
            raise EmptyPage("No sections found for this chapter.")

        # Get the previous and next chapters
        current_module = self.get_parent().specific
        chapters = list(current_module.chapters)
        current_chapter_index = chapters.index(self.specific)
        prev_chapter = chapters[current_chapter_index - 1] if current_chapter_index > 0 else None
        next_chapter = chapters[current_chapter_index + 1] if current_chapter_index < len(chapters) - 1 else None

        context.update(
            {
                "current_section": current_section,
                "prev_chapter": prev_chapter,
                "next_chapter": next_chapter,
                "current_module": current_module,  # For breadcrumbs
                "current_chapter": self.specific,  # For breadcrumbs and chapter progress
                "all_chapters": self.get_parent().specific.chapters.all().order_by("id"),  # For sidebar
                "paginated_sections": paginated_sections,  # For pagination
            }
        )

        return context


@receiver(post_save, sender=Chapter)
def parse_sections(sender, instance, created, **kwargs):
    """
    Parse and update Section instances on Chapter save.

    This handler triggers on pre-save of a Chapter instance.
    If new or modified, existing Section instances are deleted,
    and new ones are created based on the Chapter's content.

    Args:
        sender (Model): The model class sending the signal.
        instance (Chapter): The actual instance being saved.
        **kwargs: Additional keyword arguments.
    """
    has_content_changed = Chapter.objects.get(pk=instance.pk).chapter_content != instance.chapter_content

    if created or has_content_changed:
        # Remove old sections
        Section.objects.filter(chapter=instance).delete()

        # Split raw content into sections based on title markers
        raw_sections = re.split(r"\n# ", instance.chapter_content.lstrip("# "))

        # Process and create new sections
        for i, raw_section in enumerate(raw_sections, start=1):
            title, sep, section_content = raw_section.partition("\n")
            Section.objects.create(chapter=instance, title=title, content=section_content, order=i, _auto_create=True)


class Section(models.Model):
    """
    Model representing a section within a Chapter.

    Fields:
        chapter (ForeignKey): Reference to the associated Chapter.
        title (CharField): Title of the section derived from Markdown content.
        content (MarkdownField): Content of the section derived from Markdown content.
        order (PositiveIntegerField): Order of the section within the Chapter.

    Notes:
        Section objects are automatically created and deleted when a Chapter object is saved with a new `content` field
    """

    chapter = models.ForeignKey(Chapter, related_name="sections", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = MarkdownField(blank=True, null=True)
    order = models.PositiveIntegerField()
    _auto_create = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self._auto_create:
            raise NotImplementedError("Section objects cannot be saved manually.")
        super().save(*args, **kwargs)
