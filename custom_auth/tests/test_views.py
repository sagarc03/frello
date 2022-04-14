"""view test"""
from typing import Any

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls.base import reverse


@pytest.mark.parametrize(
    "data",
    [
        {},
        {
            "email": "test@local.com",
            "password": "testpassword",
            "password2": "testpassword",
        },
        {
            "username": "test",
            "password": "testpassword",
            "password2": "testpassword",
        },
        {
            "username": "test",
            "email": "test@local.com",
            "password2": "testpassword",
        },
        {
            "username": "test",
            "email": "test@local.com",
            "password": "testpassword",
        },
    ],
    ids=[
        "no_data",
        "missing_username",
        "missing_email",
        "missing_password",
        "missing_password2",
    ],
)
def test_user_cannot_resgister_with_missing_data(
    data: dict[str, Any], client: Client
) -> None:
    """
    user registration with missing data fails
    """
    response = client.post(reverse("auth:register"), data=data)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "first_request,second_request",
    [
        (
            {
                "username": "test",
                "email": "test@local.com",
                "password": "testpassword",
                "password2": "testpassword",
            },
            {
                "username": "test",
                "email": "test2@local.com",
                "password": "testpassword",
                "password2": "testpassword",
            },
        ),
        (
            {
                "username": "test",
                "email": "test@local.com",
                "password": "testpassword",
                "password2": "testpassword",
            },
            {
                "username": "test2",
                "email": "test@local.com",
                "password": "testpassword",
                "password2": "testpassword",
            },
        ),
    ],
    ids=[
        "same_username",
        "same_email",
    ],
)
@pytest.mark.django_db
def test_user_cant_register_twice_with_same_credentials(
    first_request: dict[str, Any],
    second_request: dict[str, Any],
    client: Client,
) -> None:
    """
    user registration with same credentials fails
    """
    client.post(reverse("auth:register"), data=first_request)
    response = client.post(reverse("auth:register"), data=second_request)

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_cant_register_with_mismatch_passwords(
    client: Client,
) -> None:
    """
    user login with password and password2 mismatch fails.
    """
    response = client.post(
        reverse("auth:register"),
        data={
            "username": "test",
            "email": "test@local.com",
            "password": "testpassword",
            "password2": "testpassword2",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_with_required_data_can_register(client: Client) -> None:
    """
    user registration with required data passes.
    """
    client.post(
        reverse("auth:register"),
        data={
            "username": "test",
            "email": "test@local.com",
            "password": "testpassword",
            "password2": "testpassword",
        },
    )
    assert get_user_model().objects.get(username="test")


@pytest.mark.django_db
def test_user_login_requires_username_and_password(client: Client) -> None:
    """
    user login requires username password.
    """
    response = client.post(
        reverse("auth:login"),
        data={},
    )
    assert response.status_code == 400
