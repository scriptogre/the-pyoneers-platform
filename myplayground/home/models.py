from django.shortcuts import render
from wagtail.images.models import Image, AbstractImage
from wagtail.models import Page


class HomePage(Page):
    subpage_types = ["course.Module"]

    content_panels = Page.content_panels + []

    def serve(self, request, *args, **kwargs):
        if "conversation" in request.session:
            del request.session["conversation"]

        return render(request, self.template, self.get_context(request))
