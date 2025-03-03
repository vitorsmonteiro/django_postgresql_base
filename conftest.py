import pytest

from authentication.models import User
from todo.models import Task

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
