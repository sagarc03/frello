"""set up and tear down for user test module"""
import pytest

from users.models import User

from .factory import SuperUserFactory, UserFactory


@pytest.fixture
def user() -> User:
    """Generates a user for testing"""
    return UserFactory()


@pytest.fixture
def admin() -> User:
    """Generates a user for testing"""
    return SuperUserFactory()
