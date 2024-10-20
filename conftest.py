import pytest

from authentication.models import User

pytestmark = pytest.mark.django_db

USER_EMAIL = "foo@bar.com"
USER_PASSWORD = "password"  # noqa: S105


@pytest.fixture
def user_fixture() -> User:
    """User fixture."""
    user = User(email=USER_EMAIL)
    user.set_password(USER_PASSWORD)
    user.save()
    return user
