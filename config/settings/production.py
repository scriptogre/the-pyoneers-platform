from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

ALLOWED_HOSTS = [
    "the-pyoneers-platform-service.onrender.com",  # Your Render subdomain
    "pyoneers.dev",  # Your custom domain
    "www.pyoneers.dev",  # Optional: if you also want to allow www subdomain
]
