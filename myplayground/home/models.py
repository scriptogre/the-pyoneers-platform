from wagtail.images.models import Image, AbstractImage
from wagtail.models import Page


class HomePage(Page):
    subpage_types = ["course.Module"]

    content_panels = Page.content_panels + []
