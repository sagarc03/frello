"""user authentication and registrations URLs."""
from django.urls import path

from .views import (
    add_contributor_to_project,
    add_project,
    get_project,
    index,
    landing,
)

app_name = "frello"

urlpatterns = [
    path("login/", landing, name="login"),
    path("add/", add_project, name="add"),
    path("project/<int:project_id>", get_project, name="project-page"),
    path(
        "project/<int:project_id>/contributor/add",
        add_contributor_to_project,
        name="contributor-add",
    ),
    # path("issue/<int:issue_id>", add_project, name="issue-page"),
    path("", index, name="index"),
]
