import pytest

from todo.forms import TaskForm

pytestmark = pytest.mark.django_db


class TestTaskForm:
    """Test TaskForm."""

    @staticmethod
    def test_form_valid_ok() -> None:
        """Test form with valid data."""
        data = {
            "title": "Fixture task",
            "description": "Test fixture",
            "status": "new",
        }
        form = TaskForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    @pytest.mark.parametrize(("field"), ["title", "status"])
    def test_form_missing_field(field: str) -> None:
        """Test form with valid data."""
        data = {
            "title": "Fixture task",
            "description": "Test fixture",
            "status": "new",
        }
        del data[field]
        form = TaskForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {field: ["This field is required."]}
