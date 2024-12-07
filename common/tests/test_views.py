from http import HTTPStatus

from django.test import Client
from django.urls import reverse_lazy


def test_home_view(client: Client) -> None:
    """Test home view."""
    url = reverse_lazy("common:home")
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
