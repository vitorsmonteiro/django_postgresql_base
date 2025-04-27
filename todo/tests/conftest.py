import pytest

from authentication.models import User
from todo.models import Task

pytestmark = pytest.mark.django_db


@pytest.fixture
def task_fixture(user_fixture: User) -> Task:
    """Task fixture."""
    return Task.objects.create(
        title="Fixture task",
        description="Test fixture",
        created_by=user_fixture,
        status=Task.STATUS_CHOICES["new"],
    )
