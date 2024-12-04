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

    @staticmethod
    def test_post_view_nok(client: Client, user_fixture: User) -> None:
        """Test post view with correct credentials."""
        url = reverse_lazy("authentication:login")
        response = client.post(url, data={"email": user_fixture.email})
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


class TestCreateUserView:
    """Test create_user view."""

    @staticmethod
    def test_get_view(client: Client) -> None:
        """Test get view."""
        url = reverse_lazy("authentication:create_user")
        ressponse = client.get(url)
        assert ressponse.status_code == HTTPStatus.OK

    @staticmethod
    def test_post_view_ok(client: Client) -> None:
        """Test post view ok."""
        url = reverse_lazy("authentication:create_user")
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
            "password": "123456",
        }
        response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.FOUND
        assert len(User.objects.all()) == 1
        user = User.objects.all()[0]
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.email == data["email"]

    @staticmethod
    def test_post_view_nok(client: Client) -> None:
        """Test post view with missing field."""
        url = reverse_lazy("authentication:create_user")
        data = {
            "last_name": "bar",
            "email": "foo@bar.com",
            "password": "123456",
        }
        response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.OK


class TestResetPasswordView:
    """Test reset_password view."""

    @staticmethod
    def test_get_view(client: Client, user_fixture: User) -> None:
        """Test get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("authentication:reset_password")
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_post_view_ok(client: Client, user_fixture: User) -> None:
        """Test post view ok."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        data = {"password": "foo", "password2": "foo"}
        url = reverse_lazy("authentication:reset_password")
        response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_post_view_missing_field(client: Client, user_fixture: User) -> None:
        """Test post view ok."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        data = {"password": "foo"}
        url = reverse_lazy("authentication:reset_password")
        response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.OK


class TestDeleteAccountView:
    """Test delete_account view."""

    @staticmethod
    def test_get_view(client: Client, user_fixture: User) -> None:
        """Test get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("authentication:delete_account")
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_post_view(client: Client, user_fixture: User) -> None:
        """Test get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("authentication:delete_account")
        response = client.post(url)
        assert response.status_code == HTTPStatus.FOUND
        assert len(User.objects.all()) == 0


class TestEditUserView:
    """Test edit_user view."""

    @staticmethod
    def test_get_view(client: Client, user_fixture: User) -> None:
        """Test get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("authentication:edit_user")
        ressponse = client.get(url)
        assert ressponse.status_code == HTTPStatus.OK

    @staticmethod
    def test_post_view_ok(client: Client, user_fixture: User) -> None:
        """Test post view ok."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("authentication:edit_user")
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
            "password": "123456",
        }
        response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.FOUND
        assert user_fixture.first_name == data["first_name"]
        assert user_fixture.last_name == data["last_name"]
        assert user_fixture.email == data["email"]
