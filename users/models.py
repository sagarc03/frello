"""User Application models"""
from typing import Any, List

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager for custom user model"""

    def create_user(
        self, username: str, email: str, password: str = None
    ) -> Any:
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, email: str, password: str = None
    ) -> Any:
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Custom user model"""

    username = models.CharField(
        verbose_name="Username", max_length=100, unique=True
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS: List[str] = ["email"]

    def __str__(self) -> str:
        """str for user model"""
        if self.first_name and self.last_name:
            return f"[{self.first_name} {self.last_name}]<{self.email}>"

        if self.first_name:
            return f"[{self.first_name}]<{self.email}>"

        if self.last_name:
            return f"[{self.last_name}]<{self.email}>"

        return f"<{self.email}>"

    def get_full_name(self) -> str:
        """return full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        if self.first_name:
            return self.first_name

        if self.last_name:
            return self.last_name

        return ""

    @property
    def is_staff(self) -> bool:
        """check if staff"""
        return self.is_admin

    @property
    def is_superuser(self) -> bool:
        """check if superuser"""
        return self.is_admin

    def has_perm(self, *args: Any, **kwargs: Any) -> bool:
        """check if user has named permission for given obj"""
        return self.is_admin

    def has_module_perms(self, *args: Any, **kwargs: Any) -> bool:
        """if user has module permission"""
        return self.is_admin
