from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.blocks import RichTextBlock
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel


class BlogIndexPage(Page):
    subpage_types = ["BlogPage"]
    max_count = 1

    # Include the blog pages
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        blog_posts = BlogPage.objects.live().public().order_by("-date")
        context["blog_posts"] = blog_posts
        return context


class BlogTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogPage(Page):
    parent_page_types = ["BlogIndexPage"]

    date = models.DateField("Post date")
    views = models.PositiveIntegerField(default=0)
    tags = ClusterTaggableManager(through=BlogTag, blank=True)
    intro = models.CharField(max_length=250)
    description = models.TextField()

    body = StreamField(
        [
            ("paragraph", RichTextBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("views"),
        FieldPanel("tags"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("description"),
    ]
