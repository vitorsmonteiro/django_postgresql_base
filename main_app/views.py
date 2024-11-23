from typing import ClassVar, Self

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from main_app.models import Car, Manufacturer
from main_project.settings import PAGINATION_SIZE

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
    paginate_by = PAGINATION_SIZE
    ordering: ClassVar[list[str]] = ["name"]

    def get_template_names(self: Self) -> list[str]:
        """Select template name based on query origin."""
        is_htmx = self.request.headers.get("Hx-Request")
        if is_htmx:
            self.template_name = "main_app/components/car_search_result.html"
        else:
            self.template_name = "main_app/car_list.html"
        return super().get_template_names()

    def get_queryset(self: Self) -> QuerySet[Car]:
        """Get filtered queyset."""
        is_htmx = self.request.headers.get("Hx-Request")
        search = self.request.GET.get("search", "")
        if search and is_htmx:
            self.queryset = Car.objects.filter(name__istartswith=search)
        else:
            self.queryset = Car.objects.all()
        return super().get_queryset()


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
    paginate_by = PAGINATION_SIZE
    ordering: ClassVar[list[str]] = ["name"]

    def get_template_names(self: Self) -> list[str]:
        """Select template name based on query origin."""
        is_htmx = self.request.headers.get("Hx-Request")
        if is_htmx:
            self.template_name = "main_app/components/manufacturer_search_result.html"
        else:
            self.template_name = "main_app/manufacturer_list.html"
        return super().get_template_names()

    def get_queryset(self: Self) -> QuerySet[Manufacturer]:
        """Get filtered queyset."""
        is_htmx = self.request.headers.get("Hx-Request")
        search = self.request.GET.get("search", "")
        if search and is_htmx:
            self.queryset = Manufacturer.objects.filter(name__istartswith=search)
        else:
            self.queryset = Manufacturer.objects.all()
        return super().get_queryset()


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
