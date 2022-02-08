"""dev settings"""
from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

SECRET_KEY = (
    "django-insecure-ujxlf-z4pyq=97(kgr-%s06q+do6a&2a!87bv&0e6-%y*^o(mg"
)

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django_extensions",
] + INSTALLED_APPS

SHELL_PLUS = "ipython"

EMAIL_HOST = os.environ.get("EMAIL_HOST", "mailhog")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 1025)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
