"""frello test views"""
from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls.base import reverse

from frello.models import Project


@pytest.mark.parametrize(
    "url_name, kwargs",
    [
        ("frello:index", {}),
        ("frello:project-page", {"pk": 1}),
        ("frello:issue-page", {"project_id": 1, "issue_number": 1}),
    ],
    ids=["landing-page", "project-page", "issue-page"],
)
def test_user_required_be_logged_in_to_access_page(
    url_name: str, kwargs: dict[str, Any], client: Client
) -> None:
    """
    Make user only authenticated user can login
    """
    response = client.get(reverse(url_name, kwargs=kwargs))
    assert response.status_code == 302


@pytest.mark.django_db
def test_unauthenticated_user_can_not_create_project(client: Client) -> None:
    """
    unauthenticated user can not create project
    """
    response = client.post(
        reverse("frello:add"), data={"name": "test_project"}
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_authenticated_user_can_create_project(client: Client) -> None:
    """
    authenticated user can create project
    """
    user = get_user_model().objects.create(
        username="test", email="test@local.com"
    )
    client.force_login(user)
    client.post(reverse("frello:add"), data={"name": "test_project"})
    assert Project.objects.get(name="test_project")


@pytest.mark.django_db
def test_project_owner_can_add_contributor(client: Client) -> None:
    """
    owner can add other contributor
    """
    proj_owner = get_user_model().objects.create(
        username="test", email="test@local.com"
    )
    contributor = get_user_model().objects.create(
        username="test1", email="test1@local.com"
    )
    project = Project.objects.create(name="test_project", owner=proj_owner)
    client.force_login(proj_owner)

    client.post(
        reverse("frello:contributor-add", kwargs={"project_id": project.pk}),
        data={"contributor_id": contributor.pk},
    )

    assert len(contributor.project_contributors.all()) == 1  # type: ignore


@pytest.mark.django_db
def test_project_contributor_can_add_contributor(client: Client) -> None:
    """
    contributor can add other contributor
    """
    proj_owner = get_user_model().objects.create(
        username="test", email="test@local.com"
    )
    contributor_1 = get_user_model().objects.create(
        username="test1", email="test1@local.com"
    )
    contributor_2 = get_user_model().objects.create(
        username="test2", email="test2@local.com"
    )
    project = Project.objects.create(name="test_project", owner=proj_owner)
    project.contributors.add(contributor_1)

    client.force_login(contributor_1)
    client.post(
        reverse("frello:contributor-add", kwargs={"project_id": project.pk}),
        data={"contributor_id": contributor_2.pk},
    )
    assert len(contributor_2.project_contributors.all()) == 1  # type: ignore


@pytest.mark.django_db
def test_user_not_realted_to_the_project_cant_add_contributors(
    client: Client,
) -> None:
    """
    contributor can add other contributor
    """
    proj_owner = get_user_model().objects.create(
        username="test", email="test@local.com"
    )
    contributor_1 = get_user_model().objects.create(
        username="test1", email="test1@local.com"
    )
    contributor_2 = get_user_model().objects.create(
        username="test2", email="test2@local.com"
    )
    project = Project.objects.create(name="test_project", owner=proj_owner)

    client.force_login(contributor_1)
    client.post(
        reverse("frello:contributor-add", kwargs={"project_id": project.pk}),
        data={"contributor_id": contributor_2.pk},
    )
    assert len(contributor_2.project_contributors.all()) == 0  # type: ignore


@pytest.mark.django_db
def test_project_owner_can_remove_contributor(client: Client) -> None:
    """
    owner can add other contributor
    """
    proj_owner = get_user_model().objects.create(
        username="test", email="test@local.com"
    )
    contributor = get_user_model().objects.create(
        username="test1", email="test1@local.com"
    )
    project = Project.objects.create(name="test_project", owner=proj_owner)
    project.contributors.add(contributor)
    client.force_login(proj_owner)
    client.post(
        reverse(
            "frello:contributor-remove",
            kwargs={"project_id": project.pk, "user_id": contributor.pk},
        ),
    )

    assert len(contributor.project_contributors.all()) == 0  # type: ignore


@pytest.mark.django_db
def test_project_contributor_can_remove_contributor(client: Client) -> None:
    """
    contributor can add other contributor
    """
    proj_owner = get_user_model().objects.create(
        username="test", email="test@local.com"
    )
    contributor_1 = get_user_model().objects.create(
        username="test1", email="test1@local.com"
    )
    contributor_2 = get_user_model().objects.create(
        username="test2", email="test2@local.com"
    )
    project = Project.objects.create(name="test_project", owner=proj_owner)
    project.contributors.add(contributor_1)
    project.contributors.add(contributor_2)

    client.force_login(contributor_1)
    client.post(
        reverse(
            "frello:contributor-remove",
            kwargs={"project_id": project.pk, "user_id": contributor_2.pk},
        ),
    )
    assert len(contributor_2.project_contributors.all()) == 0  # type: ignore


@pytest.mark.django_db
def test_user_not_realted_to_the_project_cant_remove_contributors(
    client: Client,
) -> None:
    """
    contributor can add other contributor
    """
    proj_owner = get_user_model().objects.create(
        username="test", email="test@local.com"
    )
    contributor_1 = get_user_model().objects.create(
        username="test1", email="test1@local.com"
    )
    contributor_2 = get_user_model().objects.create(
        username="test2", email="test2@local.com"
    )
    project = Project.objects.create(name="test_project", owner=proj_owner)
    project.contributors.add(contributor_1)

    client.force_login(contributor_2)
    client.post(
        reverse(
            "frello:contributor-remove",
            kwargs={"project_id": project.pk, "user_id": contributor_1.pk},
        ),
    )
    assert len(contributor_1.project_contributors.all()) == 1  # type: ignore
