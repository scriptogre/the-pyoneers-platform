from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # Default values - must match the values of `db` service in local.yml
        "NAME": "local_db",
        "USER": "local_user",
        "PASSWORD": "local_password",
        "HOST": "db",
        "PORT": "5432",
    }
}

SECRET_KEY = "django-insecure-q!gjpno!x-detfvv!u+pkp!mf@!j96ad6^3i2g2*i4%qh#m0!k"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405
