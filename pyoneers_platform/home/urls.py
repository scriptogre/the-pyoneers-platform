from django.urls import path

from pyoneers_platform.home.views import (
    HomeView,
    fetch_latest_discord_avatars,
    receive_gigachad_message,
    send_user_message,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("send_user_message/", send_user_message, name="send_user_message"),
    path(
        "receive_gigachad_message/",
        receive_gigachad_message,
        name="receive_gigachad_message",
    ),
    path("get_discord_members/", fetch_latest_discord_avatars, name="get_discord_members"),
]
