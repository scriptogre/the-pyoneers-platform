# projects/models.py
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock
from wagtail.models import Page


class ProjectIndexPage(Page):
    intro = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
    ]


class ProjectPage(Page):
    description = models.TextField()
    link = models.URLField()
    body = StreamField(
        [
            ("paragraph", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("link"),
        FieldPanel("body"),
    ]
