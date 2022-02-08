"""test settings"""
from django.core.management.utils import get_random_secret_key

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = True

SECRET_KEY = get_random_secret_key()

TEST_RUNNER = "django.test.runner.DiscoverRunner"

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
