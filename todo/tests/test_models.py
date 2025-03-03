import pytest

from authentication.models import User
from todo.models import Task

pytestmark = pytest.mark.django_db


def test_create_task(user_fixture: User) -> None:
    """Test create Task."""
    task = Task(
        title="Fixture task",
        description="Test fixture",
        created_by=user_fixture,
        status="new",
    )
    task.save()
    assert len(Task.objects.all()) == 1
    assert Task.objects.all()[0] == task
