"""frello views"""
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, TemplateView

from .models import Issue, Project


class LandingPage(TemplateView):
    """
    Landing page containing login and registration
    """

    template_name = "login_page.html"


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    Render renders main dashboard page
    """

    template_name = "frello/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["your_project_list"] = Project.objects.filter(  # type: ignore
            owner=self.request.user
        )
        return context


@login_required
@require_http_methods(["POST"])
def add_project(request: HttpRequest) -> HttpResponse:
    """create new project"""
    if len(request.POST.get("name", "")) == 0:
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


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """
    Project view
    """

    template_name = "frello/project_page.html"
    context_object_name = "project"

    def get_queryset(self) -> QuerySet[Any]:
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(contributors=self.request.user.pk)
        ).all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["your_project_list"] = Project.objects.filter(  # type: ignore
            owner=self.request.user
        ).all()
        context["issue_list"] = Issue.objects.filter(
            project=self.get_object(), is_delete=False
        )
        proj_contributors = get_user_model().objects.exclude(
            id__in=self.get_object().contributors.all().values_list("id"),
        )
        proj_contributors = proj_contributors.exclude(id=self.request.user.pk)
        context["other_users"] = proj_contributors
        return context


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
def issue_page(
    request: HttpRequest, project_id: int, issue_number: int
) -> HttpResponse:
    """get issue page"""
    if (
        not Project.objects.filter(pk=project_id).exists()
        or not Issue.objects.filter(
            project=Project.objects.get(pk=project_id),
            issue_number=issue_number,
        ).exists()
        or Issue.objects.get(
            project=Project.objects.get(pk=project_id),
            issue_number=issue_number,
        ).is_delete
        or (
            Issue.objects.get(
                project=Project.objects.get(pk=project_id),
                issue_number=issue_number,
            ).project.owner
            != request.user
            and request.user
            not in Issue.objects.get(
                issue_number=issue_number
            ).project.contributors.all()
        )
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
            "project": Project.objects.get(pk=project_id),
            "issue": Issue.objects.get(
                project=Project.objects.get(pk=project_id),
                issue_number=issue_number,
            ),
            "issue_status": Issue.Status.choices,
        },
    )


@require_http_methods(["POST"])
def update_issue(
    request: HttpRequest, project_id: int, issue_number: int
) -> HttpResponse:
    """update issue"""
    if (
        not Project.objects.filter(pk=project_id).exists()
        or not Issue.objects.filter(
            project=Project.objects.get(pk=project_id),
            issue_number=issue_number,
        ).exists()
        or Issue.objects.get(
            project=Project.objects.get(pk=project_id),
            issue_number=issue_number,
        ).is_delete
        or (
            Issue.objects.get(
                project=Project.objects.get(pk=project_id),
                issue_number=issue_number,
            ).project.owner
            != request.user
            and request.user
            not in Issue.objects.get(
                issue_number=issue_number
            ).project.contributors.all()
        )
    ):
        return HttpResponse(
            "issue does not exists.",
            status=404,
        )
    issue = Issue.objects.get(
        project=Project.objects.get(pk=project_id),
        issue_number=issue_number,
    )

    if "status" not in request.POST:
        return HttpResponse(
            "status missing.",
            status=404,
        )
    if "description" in request.POST:
        issue.description = request.POST["description"]
    if "status" in request.POST:
        issue.status = request.POST["status"]
    issue.save()
    return render(
        request,
        template_name="frello/issue_detail.html",
        context={
            "project": Project.objects.get(pk=project_id),
            "issue": issue,
            "issue_status": Issue.Status.choices,
        },
    )
