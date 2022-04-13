"""auth application registration"""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """User Application AppConfig"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "frello"
