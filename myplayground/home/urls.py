from django.urls import path

from myplayground.home.views import send_user_message, receive_gigachad_message

urlpatterns = [
    path("send_user_message/", send_user_message, name="send_user_message"),
    path(
        "receive_gigachad_message/",
        receive_gigachad_message,
        name="receive_gigachad_message",
    ),
]
