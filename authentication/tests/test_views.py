from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse_lazy

from authentication.models import User
from conftest import USER_EMAIL, USER_PASSWORD

pytestmark = pytest.mark.django_db


class TestLogInView:
    """Tests for login View."""

    @staticmethod
    def test_get_view(client: Client) -> None:
        """Test get request."""
        url = reverse_lazy("authentication:login")
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_post_view_ok(client: Client, user_fixture: User) -> None:
        """Test post view with correct credentials."""
        url = reverse_lazy("authentication:login")
        response = client.post(
            url, data={"email": USER_EMAIL, "password": USER_PASSWORD}
        )
        assert user_fixture.is_authenticated is True
        assert response.status_code == HTTPStatus.FOUND
