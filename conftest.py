import pytest

from authentication.models import User

pytestmark = pytest.mark.django_db

FIRST_NAME = "foo"
LAST_NAME = "bar"
USER_EMAIL = "foo@bar.com"
USER_PASSWORD = "password"  # noqa: S105


@pytest.fixture
def user_fixture() -> User:
    """User fixture."""
    user = User(first_name=FIRST_NAME, last_name=LAST_NAME, email=USER_EMAIL)
    user.set_password(USER_PASSWORD)
    user.save()
    return user
