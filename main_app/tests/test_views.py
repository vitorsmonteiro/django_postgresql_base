from http import HTTPStatus
from typing import Self

import pytest
from django.http import HttpResponse  # noqa: TCH002
from django.test import Client, RequestFactory
from django.urls import reverse_lazy

from main_app import views
from main_app.models import Car, Manufacturer

pytestmark = pytest.mark.django_db
request_factory = RequestFactory()


def test_home(client: Client) -> None:
    """Test home view."""
    url = reverse_lazy("main_app:home")
    response: HttpResponse = client.get(url)
    assert response.status_code == HTTPStatus.OK


class TestCarGenericViews:
    """Test Car model generic Class Based Views."""

    def test_car_empty_list_view(self: Self) -> None:
        """Test list view with no cars on db."""
        url = reverse_lazy("main_app:car_list")
        request = request_factory.get(url)
        response = views.ListCar.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == 0

    def test_car_list_view(self: Self) -> None:
        """Test list view."""
        man = Manufacturer(name="test")
        man.save()
        car = Car(name="test", manufacturer=man)
        car.save()
        url = reverse_lazy("main_app:car_list")
        request = request_factory.get(url)
        response = views.ListCar.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == len(Car.objects.all())
        assert response.context_data["object_list"][0] == car

    def test_car_create_view(self: Self) -> None:
        """Test create view."""
        man = Manufacturer(name="test")
        man.save()
        assert Car.objects.exists() is False
        url = reverse_lazy("main_app:car_create")
        request = request_factory.post(
            url, data={"name": "test", "manufacturer": man.pk}
        )
        response = views.CreateCar.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert len(Car.objects.all()) == 1

    def test_car_delete_view(self: Self) -> None:
        """Test delete view."""
        man = Manufacturer(name="test")
        man.save()
        car = Car(name="test", manufacturer=man)
        car.save()
        assert Car.objects.exists() is True

        url = reverse_lazy("main_app:car_delete", kwargs={"pk": car.pk})
        request = request_factory.post(url)
        response = views.DeleteCar.as_view()(request, pk=car.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert Car.objects.exists() is False

    def test_car_update_view(self: Self) -> None:
        """Test update view."""
        man = Manufacturer(name="test")
        man.save()
        car = Car(name="test", manufacturer=man)
        car.save()
        url = reverse_lazy("main_app:car_update", kwargs={"pk": car.pk})
        request = request_factory.post(url)
        response = views.UpdateCar.as_view()(
            request, pk=car.pk, data={"name": "something", "manufacturer": man.pk}
        )
        assert response.status_code == HTTPStatus.FOUND
        car.refresh_from_db()
        assert car.name == "something"
