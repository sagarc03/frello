"""frello views"""
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .models import Issue, Project


@login_required
@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    return render(
        request,
        template_name="frello/dashboard.html",
        context={
            "your_project_list": Project.objects.filter(  # type: ignore
                owner=request.user
            )
        },
    )


@require_http_methods(["GET"])
def landing(request: HttpRequest) -> HttpResponse:
    """renders landing page"""
    return render(request, template_name="login_page.html")


@login_required
@require_http_methods(["POST"])
def add_project(request: HttpRequest) -> HttpResponse:
    """create new project"""
    if "name" not in request.POST:
        return HttpResponse(
            "Please provide name for the project.",
            status=404,
        )
    name = request.POST["name"]
    description = request.POST.get("description", "")
    if Project.objects.filter(  # type: ignore
        name=name, owner=request.user
    ).exists():
        return HttpResponse(
            "Project name already exists.",
            status=404,
        )
    proj = Project(  # type: ignore
        name=name,
        description=description,
        owner=request.user,
    )
    proj.save()
    return render(
        request,
        template_name="frello/your_project_list.html",
        context={
            "your_project_list": Project.objects.filter(  # type: ignore
                owner=request.user
            )
        },
    )


@login_required
@require_http_methods(["GET"])
def get_project(request: HttpRequest, project_id: int) -> HttpResponse:
    """get project_page"""
    proj = get_object_or_404(Project, pk=project_id)

    if proj.owner != request.user:
        return HttpResponseNotFound()

    proj_contributors = get_user_model().objects.exclude(
        id__in=proj.contributors.all().values_list("id"),
    )
    proj_contributors = proj_contributors.exclude(id=request.user.pk)

    return render(
        request,
        template_name="frello/project_page.html",
        context={
            "your_project_list": Project.objects.filter(  # type: ignore
                owner=request.user
            ),
            "project": proj,
            "issue_list": Issue.objects.filter(project=proj, is_delete=False),
            "other_users": proj_contributors,
        },
    )


@login_required
@require_http_methods(["POST"])
def add_contributor_to_project(
    request: HttpRequest, project_id: int
) -> HttpResponse:
    """add contributors to project"""
    if any(key not in request.POST for key in ("contributor_id",)):
        return HttpResponse(
            "contributors and project are required",
            status=404,
        )
    try:
        proj = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse(
            "Project does not exists.",
            status=404,
        )
    try:
        user = get_user_model().objects.get(pk=request.POST["contributor_id"])
    except get_user_model().DoesNotExist:
        return HttpResponse(
            "user not found.",
            status=404,
        )
    proj.contributors.add(user)
    proj.save()
    proj_contributors = get_user_model().objects.exclude(
        id__in=proj.contributors.all().values_list("id"),
    )
    proj_contributors = proj_contributors.exclude(id=request.user.pk)
    return render(
        request,
        template_name="frello/contributor_list.html",
        context={
            "project": proj,
            "other_users": proj_contributors,
        },
    )


@login_required
@require_http_methods(["POST"])
def delete_contributor(
    request: HttpRequest, project_id: int, user_id: int
) -> HttpResponse:
    """add contributors to project"""
    try:
        proj = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse(
            "Project does not exists.",
            status=404,
        )
    try:
        user = get_user_model().objects.get(pk=user_id)
    except get_user_model().DoesNotExist:
        return HttpResponse(
            "user not found.",
            status=404,
        )
    proj.contributors.remove(user)
    proj.save()
    proj_contributors = get_user_model().objects.exclude(
        id__in=proj.contributors.all().values_list("id"),
    )
    proj_contributors = proj_contributors.exclude(id=request.user.pk)

    return render(
        request,
        template_name="frello/contributor_list.html",
        context={
            "project": proj,
            "other_users": proj_contributors,
        },
    )


@login_required
@require_http_methods(["POST"])
def add_issue(request: HttpRequest, project_id: int) -> HttpResponse:
    """add issue to project"""
    try:
        proj = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse(
            "Project does not exists.",
            status=404,
        )
    if (
        proj.owner != request.user
        and request.user not in proj.contributors.all()
    ):
        return HttpResponse(
            "Project does not exists.",
            status=404,
        )

    issue_number = Issue.objects.filter(project=proj).count()
    Issue.objects.create(  # type: ignore
        issue_number=issue_number + 1,
        project=proj,
        created_by=request.user,
        title=request.POST["title"],
        description=request.POST.get("description", ""),
    )

    proj_contributors = get_user_model().objects.exclude(
        id__in=proj.contributors.all().values_list("id"),
    )
    proj_contributors = proj_contributors.exclude(id=request.user.pk)
    return render(
        request,
        template_name="frello/issue_list.html",
        context={
            "project": proj,
            "issue_list": Issue.objects.filter(project=proj, is_delete=False),
        },
    )


@login_required
@require_http_methods(["POST"])
def delete_issue(
    request: HttpRequest, project_id: int, issue_id: int
) -> HttpResponse:
    """add issue to project"""
    try:
        proj = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return HttpResponse(
            "Project does not exists.",
            status=404,
        )
    if (
        proj.owner != request.user
        and request.user not in proj.contributors.all()
    ):
        return HttpResponse(
            "Project does not exists.",
            status=404,
        )

    try:
        issue = Issue.objects.get(pk=issue_id)
    except Issue.DoesNotExist:
        return HttpResponse(
            "Issue does not exists.",
            status=404,
        )
    issue.is_delete = True
    issue.save()
    return render(
        request,
        template_name="frello/issue_list.html",
        context={
            "project": proj,
            "issue_list": Issue.objects.filter(project=proj, is_delete=False),
        },
    )


@login_required
@require_http_methods(["GET"])
def issue_page(request: HttpRequest, issue_id: int) -> HttpResponse:
    """get issue page"""
    if (
        not Issue.objects.filter(pk=issue_id).exists()
        or Issue.objects.get(pk=issue_id).project.owner != request.user
        or request.user
        not in Issue.objects.get(pk=issue_id).project.contributors.all()
    ):
        return HttpResponse(
            "issue does not exists.",
            status=404,
        )
    return render(
        request,
        template_name="frello/issue_page.html",
        context={
            "your_project_list": Project.objects.filter(  # type: ignore
                owner=request.user
            ),
            "issue_list": Issue.objects.filter(project=proj),
            "issue": Issue.objects.get(pk=issue_id),
        },
    )
