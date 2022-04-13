"""Custom user model"""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model.

    This model behaves identically to the default user model, it exits to allow
    for customization in the future if the need arises.
    """
