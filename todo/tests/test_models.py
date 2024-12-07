import pytest

from authentication.models import User
from todo.models import Task, TaskCategory, TaskStatus

pytestmark = pytest.mark.django_db


def test_create_status() -> None:
    """Test create TaskStatus."""
    status = TaskStatus(name="Todo")
    status.save()
    assert len(TaskStatus.objects.all()) == 1
    assert TaskStatus.objects.all()[0] == status


def test_create_category() -> None:
    """Test create TaskCategory."""
    category = TaskCategory(name="Work")
    category.save()
    assert len(TaskCategory.objects.all()) == 1
    assert TaskCategory.objects.all()[0] == category


def test_create_task(
    user_fixture: User,
    todo_status_fixture: TaskStatus,
    personal_category_fixture: TaskCategory,
) -> None:
    """Test create Task."""
    task = Task(
        title="Fixture task",
        description="Test fixture",
        created_by=user_fixture,
        status=todo_status_fixture,
        category=personal_category_fixture,
    )
    task.save()
    assert len(Task.objects.all()) == 1
    assert Task.objects.all()[0] == task
