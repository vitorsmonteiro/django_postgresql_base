import pytest

from authentication.models import User

pytestmark = pytest.mark.django_db


def test_create_user() -> None:
    """Test basic user creation."""
    user = User(first_name="foo", last_name="bar", email="user@email.com")
    user.set_password("123456")
    user.save()
    assert len(User.objects.all()) == 1
