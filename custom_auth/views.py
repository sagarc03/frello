"""User views"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import User


@require_http_methods(["POST"])
def user_registration(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    if any(
        key not in request.POST or request.POST[key] == ""
        for key in ("username", "email", "password", "password2")
    ):
        return HttpResponse(
            "Please provide username, email and password(s) to register.",
            status=404,
        )

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    password2 = request.POST["password2"]

    if User.objects.filter(username=username).exists():
        return HttpResponse(
            f"User with username: {username} already exists. Try login in.",
            status=404,
        )

    if User.objects.filter(email=email).exists():
        return HttpResponse(
            f"User with email: {email} already exists. Try loging in.",
            status=404,
        )

    if password != password2:
        return HttpResponse(
            "passwords provide don't match, please resubmit.",
            status=404,
        )
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return HttpResponse(
        status=204, headers={"HX-Redirect": reverse("frello:login")}
    )


@require_http_methods(["POST"])
def user_login(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    if "username" not in request.POST or "password" not in request.POST:
        return HttpResponse(
            "Please provide both username and password to login.", status=404
        )
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(
            status=204, headers={"HX-Redirect": reverse("frello:index")}
        )
    return HttpResponse(
        "User matching the given credentials not found.", status=404
    )


@login_required
@require_http_methods(["POST"])
def user_logout(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    logout(request)
    return HttpResponse(
        status=204, headers={"HX-Redirect": reverse("frello:login")}
    )
