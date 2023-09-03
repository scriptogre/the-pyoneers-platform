from django.urls import path

from allauth.account.views import (
    LoginView,
    SignupView,
    PasswordResetView,
)

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login_form.html",
        ),
        name="login",
    ),
    path(
        "signup/",
        SignupView.as_view(
            template_name="users/signup_form.html",
        ),
        name="signup",
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
        ),
        name="password_reset",
    ),
]
