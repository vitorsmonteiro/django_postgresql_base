from typing import Any, ClassVar, Self

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    """Login form."""

    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )

    def clean(self: Self) -> dict[str, Any]:
        """Perform form validation."""
        super().clean()
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if not User.objects.filter(email=email):
            msg = {"email": "User not found"}
            raise ValidationError(msg, code="user")
        user = User.objects.filter(email=email)[0]
        if not check_password(password=password, encoded=user.password):
            msg = {"password": "Password does not match"}
            raise ValidationError(msg)
        return self.cleaned_data


class ResetPasswordForm(forms.Form):
    """Reset password form form."""

    password = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )

    def clean(self: Self) -> dict[str, Any]:
        """Perform form validation."""
        super().clean()
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            msg = {"password": "Passwords do not match"}
            raise ValidationError(msg, code="pass")
        return self.cleaned_data


class CreateUserForm(UserCreationForm):
    """Create user form."""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )

    class Meta:
        """Form meta data."""

        model = get_user_model()
        fields: ClassVar[list[str]] = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class EditUserForm(forms.ModelForm):
    """Create user form."""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    profile_image = forms.ImageField(required=False)

    class Meta:
        """Form meta data."""

        model = get_user_model()
        fields: ClassVar[list[str]] = [
            "first_name",
            "last_name",
            "email",
            "profile_image",
        ]

    def full_clean(self: Self) -> None:
        """Perform full model validation."""
        super().full_clean()
        email = self.data.get("email")

        # If user don't change email ignore error for user with this email already exist
        if self.instance.email == email:
            if "email" in self.errors:
                del self.errors["email"]
            self.cleaned_data["email"] = email


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users."""

    class Meta:
        """Class Meta dara."""

        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
