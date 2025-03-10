from uuid import uuid4

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile  # noqa: TCH002
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from authentication.forms import (
    CreateUserForm,
    EditUserForm,
    LoginForm,
    ResetPasswordForm,
)
from authentication.models import User

HOME = reverse_lazy("common:home")


def login_view(request: HttpRequest) -> HttpResponse:
    """Login view.

    Args:
        request (HttpRequest): Request

    Returns:
        HttpResponse: Response
    """
    if request.method == "GET":
        return render(request, "authentication/login_form.html")
    form = LoginForm(request.POST)
    if form.is_valid():
        user = User.objects.get(email=form.cleaned_data["email"])
        login(request, user)
        return redirect(HOME)
    return render(request, "authentication/login_form.html", {"errors": form.errors})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """Logout view.

    Args:
        request (HttpRequest): Request

    Returns:
        HttpResponse: Response
    """
    logout(request)
    return redirect(HOME)


def create_user(request: HttpRequest) -> HttpResponse:
    """Create user view.

    Args:
        request (HttpRequest): Request

    Returns:
        HttpResponse: Response
    """
    if request.method == "GET":
        return render(request, "authentication/create_user.html")
    form = CreateUserForm(request.POST, request.FILES)
    if form.is_valid():
        profile_image = form.cleaned_data.get("profile_image")
        user = User(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            profile_image=profile_image,
        )
        user.set_password(form.cleaned_data["password1"])
        user.save()
        login(request, user)
        return redirect(HOME)
    return render(request, "authentication/create_user.html", {"errors": form.errors})


@login_required
def reset_password(request: HttpRequest) -> HttpResponse:
    """Reset password view.

    Args:
        request (HttpRequest): Request

    Returns:
        HttpResponse: Response
    """
    if request.method == "GET":
        return render(request, "authentication/reset_password.html")
    form = ResetPasswordForm(request.POST)
    if form.is_valid():
        user = request.user
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(request, user)
        return render(request, "authentication/reset_password.html", {"success": True})
    return render(
        request, "authentication/reset_password.html", {"errors": form.errors}
    )


@login_required
def delete_account(request: HttpRequest) -> HttpResponse:
    """Delere user view.

    Args:
        request (HttpRequest): Request

    Returns:
        HttpResponse: Response
    """
    if request.method == "GET":
        return render(request, "authentication/delete_user.html")
    user = request.user
    user.delete()
    return redirect(HOME)


@login_required
def edit_user(request: HttpRequest) -> HttpResponse:
    """Edit user view.

    Args:
        request (HttpRequest): Request

    Returns:
        HttpResponse: Response
    """
    if request.method == "GET":
        return render(request, "authentication/edit_user.html")
    form = EditUserForm(request.POST, request.FILES)
    if form.is_valid():
        profile_image: UploadedFile = form.cleaned_data["profile_image"]
        user: User = request.user
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]
        if profile_image:
            extension = profile_image._name.split(".")[-1]  # noqa: SLF001
            profile_image._set_name(f"profile_image_{user.pk}.{extension}")  # noqa: SLF001
            user.profile_image = profile_image
        user.save()
        return redirect(HOME)
    return render(request, "authentication/edit_user.html", {"errors": form.errors})


@login_required
def generate_token(request: HttpRequest) -> HttpResponse:
    """Generate a token for user.

    Args:
        request (HttpRequest): HttpRequest object.

    Returns:
        HttpResponse: HttpResponse object.
    """
    user: User = request.user
    token = str(uuid4())
    user.token = token
    user.save()
    return render(
        request=request,
        template_name="authentication/generate_token.html",
        context={"token": token},
    )
