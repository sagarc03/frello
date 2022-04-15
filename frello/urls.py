"""user authentication and registrations URLs."""
from django.urls import path

from .views import (
    Dashboard,
    LandingPage,
    ProjectDetailView,
    add_contributor_to_project,
    add_issue,
    add_project,
    delete_contributor,
    delete_issue,
    issue_page,
    update_issue,
)

app_name = "frello"

urlpatterns = [
    path("login/", LandingPage.as_view(), name="login"),
    path("add/", add_project, name="add"),
    path("project/<int:pk>", ProjectDetailView.as_view(), name="project-page"),
    path(
        "project/<int:project_id>/contributor/add/",
        add_contributor_to_project,
        name="contributor-add",
    ),
    path(
        "project/<int:project_id>/contributor/<int:user_id>/remove/",
        delete_contributor,
        name="contributor-remove",
    ),
    path(
        "project/<int:project_id>/issue/add/",
        add_issue,
        name="issue-add",
    ),
    path(
        "project/<int:project_id>/issue/<int:issue_id>/delete/",
        delete_issue,
        name="issue-delete",
    ),
    path(
        "project/<int:project_id>/issue/<int:issue_number>/update",
        update_issue,
        name="issue-update",
    ),
    path(
        "project/<int:project_id>/issue/<int:issue_number>/",
        issue_page,
        name="issue-page",
    ),
    path("", Dashboard.as_view(), name="index"),
]
