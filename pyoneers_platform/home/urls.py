from django.urls import path

from pyoneers_platform.home.views import HomeView, fetch_gigachad_gpt_response, fetch_latest_discord_avatars

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "fetch_gigachad_gpt_response/",
        fetch_gigachad_gpt_response,
        name="fetch_gigachad_gpt_response",
    ),
    path("fetch_discord_members/", fetch_latest_discord_avatars, name="fetch_discord_members"),
]
