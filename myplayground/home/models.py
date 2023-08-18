from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from myplayground.blog.models import BlogPage


class HomePage(Page):
    max_count = 1

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    # Get the latest blog posts.
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        # Adjust this query to your needs, e.g. filter, order_by, etc.
        blog_posts = BlogPage.objects.live().public().order_by("-date")[:5]
        context["blog_posts"] = blog_posts
        return context
