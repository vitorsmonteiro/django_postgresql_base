import pytest

from authentication.models import User
from todo.models import Task

pytestmark = pytest.mark.django_db

FIRST_NAME = "foo"
LAST_NAME = "bar"
USER_EMAIL = "foo@bar.com"
USER_PASSWORD = "password"  # noqa: S105
TOKEN = "foo"  # noqa: S105


@pytest.fixture
def user_fixture() -> User:
    """User fixture."""
    user = User(
        first_name=FIRST_NAME, last_name=LAST_NAME, email=USER_EMAIL, token=TOKEN
    )
    user.set_password(USER_PASSWORD)
    user.save()
    return user


@pytest.fixture
def user_fixture2() -> User:
    """User fixture 2."""
    user = User(first_name="foo", last_name="bar", email="foobar@mail.com", token="bar")  # noqa: S106
    user.set_password(USER_PASSWORD)
    user.save()
    return user


@pytest.fixture
def task_fixture(user_fixture: User) -> Task:
    """Task fixture."""
    task = Task(
        title="Fixture task",
        description="Test fixture",
        created_by=user_fixture,
        status=Task.STATUS_CHOICES["new"],
    )
    task.save()
    return task
