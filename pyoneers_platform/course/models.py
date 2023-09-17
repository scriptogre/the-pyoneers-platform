from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtailmarkdown.blocks import MarkdownBlock
from wagtailmarkdown.fields import MarkdownField


class ModuleIndex(Page):
    description = MarkdownField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]


class ChapterBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    icon = blocks.CharBlock(default="list-ul")
    content = MarkdownBlock(icon="code")

    class Meta:
        icon = "list-ul"
        label = "Chapter"


class Module(Page):
    description = MarkdownField(blank=True, null=True)

    body = StreamField(
        [
            ("chapter", ChapterBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("body"),
    ]
