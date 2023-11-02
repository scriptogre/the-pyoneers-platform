from django.urls import path

from pyoneers_platform.course.views import redirect_to_first_section, section_view
from pyoneers_platform.course.webhooks import handle_github_webhook

app_name = "course"

urlpatterns = [
    path("github-webhook/", handle_github_webhook),
    path("<slug:chapter_slug>/", redirect_to_first_section, name="chapter"),
    path("<slug:chapter_slug>/<slug:section_slug>/", section_view, name="section"),
]
