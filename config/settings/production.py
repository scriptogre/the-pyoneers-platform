from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # Default values for local development (same as the values from local.yml)
        # Overridden in production by setting env variables
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

ALLOWED_HOSTS = [
    "the-pyoneers-platform-service.onrender.com",  # Your Render subdomain
    "pyoneers.dev",  # Your custom domain
    "www.pyoneers.dev",  # Optional: if you also want to allow www subdomain
]
