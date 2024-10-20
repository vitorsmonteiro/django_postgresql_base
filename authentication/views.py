from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from authentication.forms import CreateUserForm, LoginForm, ResetPasswordForm

User = get_user_model()
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
    form = CreateUserForm(request.POST)
    if form.is_valid():
        user = User(email=form.cleaned_data["email"])
        user.set_password(form.cleaned_data["password"])
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
