import pytest

from authentication.models import User
from todo.models import Task, TaskCategory, TaskStatus

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
def todo_status_fixture() -> TaskStatus:
    """Todo status fixture."""
    status = TaskStatus(name="Todo")
    status.save()
    return status


@pytest.fixture
def in_progress_status_fixture() -> TaskStatus:
    """In progress status fixture."""
    status = TaskStatus(name="In Progress")
    status.save()
    return status


@pytest.fixture
def done_status_fixture() -> TaskStatus:
    """Done status fixture."""
    status = TaskStatus(name="Done")
    status.save()
    return status


@pytest.fixture
def personal_category_fixture() -> TaskCategory:
    """Personal category fixture."""
    category = TaskCategory(name="Personal")
    category.save()
    return category


@pytest.fixture
def work_category_fixture() -> TaskCategory:
    """Work category fixture."""
    category = TaskCategory(name="Work")
    category.save()
    return category


@pytest.fixture
def task_fixture(
    user_fixture: User,
    todo_status_fixture: TaskStatus,
    personal_category_fixture: TaskCategory,
) -> Task:
    """Task fixture."""
    task = Task(
        title="Fixture task",
        description="Test fixture",
        created_by=user_fixture,
        status=todo_status_fixture,
        category=personal_category_fixture,
    )
    task.save()
    return task
