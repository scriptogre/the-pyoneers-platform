"""
Defines Chapter and Section models for a Django app. These models are auto-populated by a GitHub repository
via webhooks.

Models:
    - Chapter: Represents a chapter in a course.
    - Section: Represents a section in a chapter.
"""

from django.db import models
from django.urls import reverse


class Chapter(models.Model):
    """Represents a course chapter. Auto-populated via GitHub webhook."""

    order = models.IntegerField()
    slug = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    @property
    def previous(self):
        """Returns the previous chapter in the course, or None if this is the first chapter."""
        return Chapter.objects.filter(order__lt=self.order).order_by("-order").first()

    @property
    def next(self):
        """Returns the next chapter in the course, or None if this is the last chapter."""
        return Chapter.objects.filter(order__gt=self.order).order_by("order").first()

    @property
    def url(self):
        return self.get_absolute_url()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course:chapter", args=[str(self.slug)])

    def get_last_section(self):
        return self.sections.last()


class Section(models.Model):
    """Represents a section within a Chapter. Auto-populated via GitHub webhook."""

    chapter = models.ForeignKey(Chapter, related_name="sections", on_delete=models.CASCADE)

    order = models.IntegerField()
    slug = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()

    @property
    def previous(self):
        """Returns the previous section in the chapter, or None if this is the first section."""
        return self.chapter.sections.filter(order__lt=self.order).order_by("-order").first()

    @property
    def next(self):
        """Returns the next section in the chapter, or None if this is the last section."""
        return self.chapter.sections.filter(order__gt=self.order).order_by("order").first()

    @property
    def url(self):
        return self.get_absolute_url()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course:section", args=[str(self.chapter.slug), str(self.slug)])

    class Meta:
        ordering = ["order"]
        unique_together = ["chapter", "order"]
