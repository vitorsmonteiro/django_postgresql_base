import pytest

from authentication.forms import (
    CreateUserForm,
    EditUserForm,
    LoginForm,
    ResetPasswordForm,
)
from authentication.models import User
from conftest import USER_PASSWORD

pytestmark = pytest.mark.django_db


class TestCreateUserForm:
    """Test CreateUserForm."""

    @staticmethod
    def test_create_user_form_ok() -> None:
        """Test form with good data."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
            "password": "123456",
        }
        form = CreateUserForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    def test_create_user_form_missing_first_name() -> None:
        """Test form with good missing first_name."""
        data = {
            "last_name": "bar",
            "email": "foo@bar.com",
            "password": "123456",
        }
        form = CreateUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"first_name": ["This field is required."]}

    @staticmethod
    def test_create_user_form_missing_last_name() -> None:
        """Test form with good missing last_name."""
        data = {
            "first_name": "foo",
            "email": "foo@bar.com",
            "password": "123456",
        }
        form = CreateUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"last_name": ["This field is required."]}

    @staticmethod
    def test_create_user_form_missing_email() -> None:
        """Test form with good missing email."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "password": "123456",
        }
        form = CreateUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"email": ["This field is required."]}

    @staticmethod
    def test_create_user_form_missing_password() -> None:
        """Test form with good missing password."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
        }
        form = CreateUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"password": ["This field is required."]}

    @staticmethod
    def test_create_user_form_invalid_email() -> None:
        """Test form with good data."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foobar.com",
            "password": "123456",
        }
        form = CreateUserForm(data=data)
        assert form.is_valid() is False


class TestLoginForm:
    """Test LoginForm."""

    @staticmethod
    def test_login_ok(user_fixture: User) -> None:
        """Test login ok."""
        data = {"email": user_fixture.email, "password": USER_PASSWORD}
        form = LoginForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    def test_login_wrong_email(user_fixture: User) -> None:
        """Test login wrong email."""
        data = {"email": user_fixture.email + "2", "password": USER_PASSWORD}
        form = LoginForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"email": ["User not found"]}

    @staticmethod
    def test_login_wrong_password(user_fixture: User) -> None:
        """Test login wrong password."""
        data = {"email": user_fixture.email, "password": USER_PASSWORD + "2"}
        form = LoginForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"password": ["Password does not match"]}

    @staticmethod
    def test_login_missing_email() -> None:
        """Test login with missing email."""
        data = {"password": USER_PASSWORD + "2"}
        form = LoginForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"email": ["This field is required.", "User not found"]}

    @staticmethod
    def test_login_missing_password(user_fixture: User) -> None:
        """Test login with missing password."""
        data = {"email": user_fixture.email}
        form = LoginForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {
            "password": ["This field is required.", "Password does not match"]
        }


class TestResetPasswordForm:
    """Test ResetPasswordForm."""

    @staticmethod
    def test_reset_password_ok() -> None:
        """Test reset password form ok."""
        data = {"password": "foo", "password2": "foo"}
        form = ResetPasswordForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    def test_reset_password_missing_password() -> None:
        """Test reset password form with missing password."""
        data = {"password2": "foo"}
        form = ResetPasswordForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {
            "password": ["This field is required.", "Passwords do not match"]
        }

    @staticmethod
    def test_reset_password_missing_password2() -> None:
        """Test reset password form with missing password2."""
        data = {"password": "foo"}
        form = ResetPasswordForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {
            "password2": ["This field is required."],
            "password": ["Passwords do not match"],
        }

    @staticmethod
    def test_reset_password_missmatch() -> None:
        """Test reset password form with not matching passwords."""
        data = {"password": "foo", "password2": "bar"}
        form = ResetPasswordForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"password": ["Passwords do not match"]}


class TestEditUserForm:
    """Test CreateUserForm."""

    @staticmethod
    def test_edit_user_form_ok() -> None:
        """Test form with good data."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
            "profile_image": "test.jpeg",
        }
        form = EditUserForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    def test_edit_user_form_missing_first_name() -> None:
        """Test form with good missing first_name."""
        data = {
            "last_name": "bar",
            "email": "foo@bar.com",
        }
        form = EditUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"first_name": ["This field is required."]}

    @staticmethod
    def test_edit_user_form_missing_last_name() -> None:
        """Test form with good missing last_name."""
        data = {
            "first_name": "foo",
            "email": "foo@bar.com",
        }
        form = EditUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"last_name": ["This field is required."]}

    @staticmethod
    def test_edit_user_form_missing_email() -> None:
        """Test form with good missing email."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
        }
        form = EditUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"email": ["This field is required."]}

    @staticmethod
    def test_edit_user_form_invalid_email() -> None:
        """Test form with good data."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foobar.com",
        }
        form = EditUserForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"email": ["Enter a valid email address."]}

    @staticmethod
    def test_edit_user_form_existing_email(user_fixture: User) -> None:
        """Test form with good data."""
        data = {
            "first_name": "foo",
            "last_name": "bar",
            "email": user_fixture.email,
            "profile_image": "test.jpeg",
        }
        form = EditUserForm(data=data)
        assert form.is_valid() is True
