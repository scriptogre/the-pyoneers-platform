from django.urls import path

from myplayground.home.views import user_chat_response

urlpatterns = [
    path("chat_response/", user_chat_response, name="chat_response"),
]
