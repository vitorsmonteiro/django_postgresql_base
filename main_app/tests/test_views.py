from http import HTTPStatus

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


class TestManufacturerGenericViews:
    """Test Car model generic Class Based Views."""

    @staticmethod
    def test_manufacturer_empty_list_view() -> None:
        """Test list view with no manufacturer on db."""
        url = reverse_lazy("main_app:manufacturer_list")
        request = request_factory.get(url)
        response = views.ListManufacturer.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == 0

    @staticmethod
    def test_manufacturer_list_view() -> None:
        """Test manufacturer view."""
        man = Manufacturer(name="test")
        man.save()
        url = reverse_lazy("main_app:car_list")
        request = request_factory.get(url)
        response = views.ListManufacturer.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == len(
            Manufacturer.objects.all()
        )
        assert response.context_data["object_list"][0] == man

    @staticmethod
    def test_manufacturer_create_view() -> None:
        """Test create view."""
        assert Manufacturer.objects.exists() is False
        url = reverse_lazy("main_app:manufacturer_create")
        request = request_factory.post(url, data={"name": "test"})
        response = views.CreateManufacturer.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert len(Manufacturer.objects.all()) == 1

    @staticmethod
    def test_manufacturer_delete_view() -> None:
        """Test delete view."""
        man = Manufacturer(name="test")
        man.save()
        assert Manufacturer.objects.exists() is True

        url = reverse_lazy("main_app:manufacturer_delete", kwargs={"pk": man.pk})
        request = request_factory.post(url)
        response = views.DeleteManufacturer.as_view()(request, pk=man.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert Manufacturer.objects.exists() is False

    @staticmethod
    def test_manufacturer_update_view(client: Client) -> None:
        """Test update view."""
        man = Manufacturer(name="test")
        man.save()
        url = reverse_lazy("main_app:manufacturer_update", kwargs={"pk": man.pk})
        response = client.post(url, data={"name": "something"})
        man.refresh_from_db()
        assert response.status_code == HTTPStatus.FOUND
        assert man.name == "something"


class TestCarGenericViews:
    """Test Car model generic Class Based Views."""

    @staticmethod
    def test_car_empty_list_view() -> None:
        """Test list view with no cars on db."""
        url = reverse_lazy("main_app:car_list")
        request = request_factory.get(url)
        response = views.ListCar.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == 0

    @staticmethod
    def test_car_list_view() -> None:
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

    @staticmethod
    def test_car_create_view() -> None:
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

    @staticmethod
    def test_car_delete_view() -> None:
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

    @staticmethod
    def test_car_update_view(client: Client) -> None:
        """Test update view."""
        man = Manufacturer(name="test")
        man.save()
        car = Car(name="test", manufacturer=man)
        car.save()
        url = reverse_lazy("main_app:car_update", kwargs={"pk": car.pk})
        response = client.post(url, data={"name": "something", "manufacturer": man.pk})
        assert response.status_code == HTTPStatus.FOUND
        car.refresh_from_db()
        assert car.name == "something"
