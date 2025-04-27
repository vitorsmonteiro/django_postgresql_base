import pytest

from authentication.models import User
from todo.models import Task

pytestmark = pytest.mark.django_db


def test_create_task(user_fixture: User) -> None:
    """Test create Task."""
    assert Task.objects.exists() is False
    task = Task.objects.create(
        title="Fixture task",
        description="Test fixture",
        created_by=user_fixture,
        status="new",
    )
    assert Task.objects.exists() is True
    assert Task.objects.first() == task
