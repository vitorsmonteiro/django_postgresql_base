from typing import Any, ClassVar, Self

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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
        if not User.objects.filter(email=email, password=password):
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


class CreateUserForm(forms.ModelForm):
    """Create user form."""

    name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )

    class Meta:
        """Form meta data."""

        model = get_user_model()
        fields: ClassVar[list[str]] = ["name", "email", "password"]

    def clean(self: Self) -> dict[str, Any]:
        """Perform form validation."""
        super().clean()
        email = self.cleaned_data.get("email")
        validate_email(email)
        return self.cleaned_data
