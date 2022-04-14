"""frello views"""
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    return render(request, template_name="frello/dashboard.html")


@require_http_methods(["GET"])
def landing(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    return render(request, template_name="login_page.html")
