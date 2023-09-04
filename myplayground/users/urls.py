from django.urls import path

from myplayground.users.views import UserDetailView

app_name = "users"

urlpatterns = [
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
]
