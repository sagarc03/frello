"""User application registration."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """User Application AppConfig"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
