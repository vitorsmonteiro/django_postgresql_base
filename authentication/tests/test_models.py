import pytest

from authentication.models import User

pytestmark = pytest.mark.django_db


def test_create_user() -> None:
    """Test basic user creation."""
    assert User.objects.exists() is False
    user = User(first_name="foo", last_name="bar", email="user@email.com")
    user.set_password("Test*123456")
    user.save()
    assert User.objects.exists() is True


def test_delete_user(user_fixture: User) -> None:
    """Test basic user delete."""
    assert User.objects.exists() is True
    user_fixture.delete()
    assert User.objects.exists() is False



class TestUserManager:
    """Test UserManager."""

    @staticmethod
    def test_create_user() -> None:
        """Test basic user creation with UserManager."""
        assert User.objects.exists() is False
        user: User = User.objects.create_user(
            first_name="foo",
            last_name="bar",
            email="user@email.com",
            password="Test*123456",  # noqa: S106
        )
        assert User.objects.exists() is True
        assert user.is_staff is False
        assert user.is_superuser is False

    @staticmethod
    def test_create_user_without_email() -> None:
        """Test basic user creation with UserManager without email."""
        with pytest.raises(ValueError, match="Users must have an email address."):
            User.objects.create_user(
                first_name="foo",
                last_name="bar",
                email="",
                password="Test*123456",  # noqa: S106
            )

    @staticmethod
    def test_create_superuser() -> None:
        """Test superuser creation with UserManager."""
        assert User.objects.exists() is False
        user: User = User.objects.create_superuser(
            first_name="foo",
            last_name="bar",
            email="user@email.com",
            password="Test*123456",  # noqa: S106
        )
        assert User.objects.exists() is True
        assert user.is_staff is True
        assert user.is_superuser is True
