"""frello views"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    return render(request, template_name="landing_page.html")
