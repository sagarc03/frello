"""user authentication and registrations URLs."""
from django.urls import path

from .views import index, landing

app_name = "frello"

urlpatterns = [
    path("login/", landing, name="login"),
    path("", index, name="index"),
]
