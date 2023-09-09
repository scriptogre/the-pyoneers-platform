from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Parse database configuration directly from $DATABASE_URL
DATABASES = {"default": env.db("DATABASE_URL")}

ALLOWED_HOSTS = [
    "the-pyoneers-platform-service.onrender.com",  # Your Render subdomain
    "pyoneers.dev",  # Your custom domain
    "www.pyoneers.dev",  # Optional: if you also want to allow www subdomain
]


# This is to ensure that Django uses https:// instead of http:// in URLs
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
