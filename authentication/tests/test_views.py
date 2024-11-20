from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse_lazy

from authentication.models import User
from conftest import USER_PASSWORD

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
            url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        assert response.status_code == HTTPStatus.FOUND
        reset_pass_url = reverse_lazy("authentication:reset_password")
        response = client.get(reset_pass_url)
        assert response.status_code == HTTPStatus.OK


class TestLogOutView:
    """Tests for logout View."""

    @staticmethod
    def test_get_view(client: Client, user_fixture: User) -> None:
        """Test get request."""
        login_url = reverse_lazy("authentication:login")
        response = client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        logout_url = reverse_lazy("authentication:logout")
        response = client.get(logout_url)
        assert response.status_code == HTTPStatus.FOUND
        reset_pass_url = reverse_lazy("authentication:reset_password")
        response = client.get(reset_pass_url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/reset_password"
