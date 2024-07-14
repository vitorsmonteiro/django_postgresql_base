from typing import ClassVar

from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from main_app.models import Car, Manufacturer

CAR_LIST_URL = reverse_lazy("main_app:car_list")
MAN_LIST_URL = reverse_lazy("main_app:manufacturer_list")


def home(request: HttpRequest) -> HttpResponse:
    """Home view for the main app.

    Args:
        request (HttpRequest): _Hettp request from client.

    Returns:
        HttpResponse: Http response from server.
    """
    return HttpResponse(f"Hello {request.user}")


class ListCar(ListView):
    """List all Car models."""

    model = Car


class CreateCar(CreateView):
    """Create Car model view."""

    model = Car
    fields: ClassVar[list[str]] = ["name", "manufacturer"]
    success_url = CAR_LIST_URL


class UpdateCar(UpdateView):
    """Update Car model view."""

    model = Car
    fields: ClassVar[list[str]] = ["name", "manufacturer"]
    success_url = CAR_LIST_URL


class DeleteCar(DeleteView):
    """Delete Car model view."""

    model = Car
    success_url = CAR_LIST_URL


class ListManufacturer(ListView):
    """List all Manufacturer models."""

    model = Manufacturer


class CreateManufacturer(CreateView):
    """Create Manufacturer model view."""

    model = Manufacturer
    fields: ClassVar[list[str]] = ["name"]
    success_url = MAN_LIST_URL


class UpdateManufacturer(UpdateView):
    """Update Manufacturer model view."""

    model = Manufacturer
    fields: ClassVar[list[str]] = ["name"]
    success_url = MAN_LIST_URL


class DeleteManufacturer(DeleteView):
    """Delete Manufacturer model view."""

    model = Manufacturer
    success_url = MAN_LIST_URL
