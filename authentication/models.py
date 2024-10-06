from typing import ClassVar, Self

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom User manager."""

    def create_user(self: Self, email: str, password: str) -> AbstractBaseUser:
        """Create and saves a User with the given email and password.

        Args:
            email (str): Email
            password (str): Password.

        Raises:
            ValueError: If email is empty

        Returns:
            User: User instance.
        """
        if not email:
            msg = "Users must have an email address."
            raise ValueError(msg)

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self: Self, email: str, password: str) -> AbstractBaseUser:
        """Create and saves a superser with the given email and password.

        Args:
            email (str): Email
            password (str): Password.

        Raises:
            ValueError: If email is empty

        Returns:
            User: User instance.
        """
        if not email:
            msg = "Users must have an email address."
            raise ValueError(msg)

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    """Custom User Model."""

    email = models.EmailField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    objects = UserManager()
    is_staff = models.BooleanField(default=False, blank=True)
    is_superuser = models.BooleanField(default=False, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    def __str__(self: Self) -> str:
        """String representation."""
        return f"{self.email}"
