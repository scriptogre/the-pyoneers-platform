from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView

from pyoneers_platform.course.models import Chapter, Section


class SectionDetailView(DetailView):
    model = Section
    context_object_name = "section"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_chapters"] = Chapter.objects.all().order_by("order")

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Section, slug=self.kwargs["section_slug"], chapter__slug=self.kwargs["chapter_slug"])


section_view = SectionDetailView.as_view()


def redirect_to_first_section(request, chapter_slug):
    chapter = get_object_or_404(Chapter, slug=chapter_slug)
    first_section = chapter.sections.first()
    return redirect(first_section)
