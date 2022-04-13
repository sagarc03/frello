"""user authentication and registrations URLs."""
from django.urls import path

from .views import index

app_name = "frello"

urlpatterns = [
    path("", index, name="index"),
]
