from typing import ClassVar, Self

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom User manager."""

    def create_user(
        self: Self, email: str, password: str, first_name: str, last_name: str
    ) -> AbstractBaseUser:
        """Create and saves a User with the given email and password.

        Args:
            email (str): Email
            password (str): Password.
            first_name (str): First name.
            last_name (str): Last name.

        Raises:
            ValueError: If email is empty

        Returns:
            User: User instance.
        """
        if not email:
            msg = "Users must have an email address."
            raise ValueError(msg)

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self: Self, email: str, password: str, first_name: str, last_name: str
    ) -> AbstractBaseUser:
        """Create and saves a superser with the given email and password.

        Args:
            email (str): Email
            password (str): Password.
            first_name (str): First name.
            last_name (str): Last name.

        Raises:
            ValueError: If email is empty

        Returns:
            User: User instance.
        """
        user = self.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    """Custom User Model."""

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_image = models.ImageField(
        upload_to="static/authentication/img/",
        default="static/authentication/img/blank_profile.jpg",
    )
    objects = UserManager()
    is_staff = models.BooleanField(default=False, blank=True)
    is_superuser = models.BooleanField(default=False, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    def __str__(self: Self) -> str:
        """String representation."""
        return f"{self.email}"
