"""user authentication and registrations URLs."""
from django.urls import path

from .views import user_login, user_logout, user_registration

app_name = "auth"

urlpatterns = [
    path("register/", user_registration, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
]
