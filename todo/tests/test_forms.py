import pytest

from authentication.models import User
from todo.forms import TaskCategoryForm, TaskForm, TaskStatusForm
from todo.models import TaskCategory, TaskStatus

pytestmark = pytest.mark.django_db


class TestTaskStatusForm:
    """Test TaskStatusForm."""

    @staticmethod
    def test_form_valid_ok() -> None:
        """Test form with valid data."""
        data = {"name": "Stauts"}
        form = TaskStatusForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    def test_form_missing_field() -> None:
        """Test form validation with missing field."""
        form = TaskStatusForm(data={})
        assert form.is_valid() is False
        assert form.errors == {"name": ["This field is required."]}


class TestTaskCategoryForm:
    """Test TaskCategoryForm."""

    @staticmethod
    def test_form_valid_ok() -> None:
        """Test form with valid data."""
        data = {"name": "Stauts"}
        form = TaskCategoryForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    def test_form_missing_field() -> None:
        """Test form validation with missing field."""
        form = TaskCategoryForm(data={})
        assert form.is_valid() is False
        assert form.errors == {"name": ["This field is required."]}


class TestTaskForm:
    """Test TaskForm."""

    @staticmethod
    def test_form_valid_ok(
        user_fixture: User,
        todo_status_fixture: TaskStatus,
        personal_category_fixture: TaskCategory,
    ) -> None:
        """Test form with valid data."""
        data = {
            "title": "Fixture task",
            "description": "Test fixture",
            "created_by": user_fixture.pk,
            "status": todo_status_fixture.pk,
            "category": personal_category_fixture.pk,
        }
        form = TaskForm(data=data)
        assert form.is_valid() is True
