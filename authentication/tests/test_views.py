import shutil
from http import HTTPStatus
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse_lazy

from authentication.models import User
from authentication.tests.fixtures import USER_PASSWORD
from main_project.settings import MEDIA_ROOT

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
    def teardown_method() -> None:
        """Called after each test method to celan up folder."""
        path = Path(MEDIA_ROOT)
        if path.exists and path.is_dir:
            shutil.rmtree(path=path)

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
        path = Path().cwd()
        path = (
            path
            / "authentication"
            / "static"
            / "authentication"
            / "img"
            / "blank_profile.jpg"
        )
        with path.open("rb") as file:
            image = SimpleUploadedFile(
                "image.jpg", file.read(), content_type="image/jpeg"
            )
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
            "password1": "123456*Test",
            "password2": "123456*Test",
            "profile_image": image,
        }
        response = client.post(url, data=data)
        user = User.objects.first()
        stored_image = Path(user.profile_image.storage.location)
        stored_image = stored_image / user.profile_image.name
        assert response.status_code == HTTPStatus.FOUND
        assert len(User.objects.all()) == 1
        user = User.objects.all()[0]
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
        assert user.email == data["email"]
        assert stored_image.exists() is True
        stored_image.unlink()

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
    def teardown_method() -> None:
        """Called after each test method to celan up folder."""
        path = Path(MEDIA_ROOT)
        if path.exists and path.is_dir:
            shutil.rmtree(path=path)

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
        path = Path.cwd()
        path = (
            path
            / "authentication"
            / "static"
            / "authentication"
            / "img"
            / "blank_profile.jpg"
        )
        with path.open("rb") as img:
            data = {
                "first_name": "foo",
                "last_name": "bar",
                "email": "foo@bar.com",
                "profile_image": img,
            }
            response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.FOUND
        assert user_fixture.first_name == data["first_name"]
        assert user_fixture.last_name == data["last_name"]
        assert user_fixture.email == data["email"]

    @staticmethod
    def test_post_view_nok(client: Client, user_fixture: User) -> None:
        """Test post view invalid form."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("authentication:edit_user")
        data = {
            "first_name": "foo",
            "last_name": "bar",
        }
        response = client.post(url, data=data)
        assert response.status_code == HTTPStatus.OK
        assert "email: This field is required." in str(response.content)


class TestGenerateTokenView:
    """Tests for generate_token view."""

    @staticmethod
    def test_token_generation(client: Client, user_fixture: User) -> None:
        """Test generation of a new token."""
        user_fixture.token = ""
        user_fixture.save()
        user_fixture.refresh_from_db()
        assert user_fixture.token == ""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("authentication:generate_token")
        response = client.get(url)
        user_fixture.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert user_fixture.token != ""
