"""Model factory"""
import random
import string

import factory
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    """Custom user factory for testing"""

    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda o: f"{o.first_name}.{o.last_name[0]}"
    )
    email = factory.LazyAttribute(
        lambda o: f"{o.first_name}.{o.last_name}@test.longboardfunds.com"
    )
    password = factory.PostGenerationMethodCall(
        "set_password",
        "".join([random.choice(string.ascii_letters) for _ in range(20)]),
    )


class SuperUserFactory(DjangoModelFactory):
    """Custom super user factory for testing"""

    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda o: f"{o.first_name}.{o.last_name[0]}"
    )
    email = factory.LazyAttribute(
        lambda o: f"{o.first_name}.{o.last_name}@test.longboardfunds.com"
    )
    is_admin = True
    password = factory.PostGenerationMethodCall(
        "set_password",
        "".join([random.choice(string.ascii_letters) for _ in range(20)]),
    )
