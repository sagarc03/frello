"""Test users models"""
import pytest

from users.models import User


@pytest.mark.django_db
def test_all_permission_regular_user(user: User) -> None:
    """user object has permission for everything"""
    assert not user.has_perm()


@pytest.mark.django_db
def test_all_module_permission_regular_user(user: User) -> None:
    """user object has permission for all application"""
    assert not user.has_module_perms()


@pytest.mark.django_db
def test_all_permission_super_user(admin: User) -> None:
    """user object has permission for everything"""
    assert admin.has_perm()


@pytest.mark.django_db
def test_all_module_permission_super_user(admin: User) -> None:
    """user object has permission for all application"""
    assert admin.has_module_perms()


def test_str_no_first_last_name() -> None:
    """str with only email"""
    obj = User(username="test", email="test@test.com")
    assert str(obj) == "<test@test.com>"


def test_str_no_last_name() -> None:
    """str with email and first name"""
    obj = User(username="test", email="test@test.com", first_name="first")
    assert str(obj) == "[first]<test@test.com>"


def test_str_no_first_name() -> None:
    """str with email and last name"""
    obj = User(username="test", email="test@test.com", last_name="last")
    assert str(obj) == "[last]<test@test.com>"


def test_str_all_data() -> None:
    """str with all data"""
    obj = User(
        username="test",
        email="test@test.com",
        first_name="first",
        last_name="last",
    )
    assert str(obj) == "[first last]<test@test.com>"


def test_get_full_name_no_first_name_no_last_name() -> None:
    """should return empty string"""
    obj = User(username="test", email="test@test.com")
    assert obj.get_full_name() == ""


def test_get_full_name_first_name_no_last_name() -> None:
    """should return first name only"""
    obj = User(username="test", email="test@test.com", first_name="first")
    assert obj.get_full_name() == "first"


def test_get_full_name_no_first_name_last_name() -> None:
    """should return last name only"""
    obj = User(username="test", email="test@test.com", last_name="last")
    assert obj.get_full_name() == "last"


def test_get_full_name_first_name_last_name() -> None:
    """should return first name and last name"""
    obj = User(
        username="test",
        email="test@test.com",
        first_name="first",
        last_name="last",
    )
    assert obj.get_full_name() == "first last"
