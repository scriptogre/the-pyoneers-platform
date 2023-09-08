from django.urls import path

from pyoneers_platform.home.views import (
    send_user_message,
    receive_gigachad_message,
    HomeView,
    get_latest_discord_members,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("send_user_message/", send_user_message, name="send_user_message"),
    path(
        "receive_gigachad_message/",
        receive_gigachad_message,
        name="receive_gigachad_message",
    ),
    path(
        "get_discord_members/", get_latest_discord_members, name="get_discord_members"
    ),
]
