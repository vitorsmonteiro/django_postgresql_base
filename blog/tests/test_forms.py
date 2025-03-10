import pytest

from blog.forms import TopicForm
from blog.models import Topic

pytestmark = pytest.mark.django_db


class TestTopicForm:
    """Test TopicForm."""

    @staticmethod
    def test_topic_form() -> None:
        """Test topic form with valid data."""
        data = {"name": "topic"}
        form = TopicForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    def test_topic_form_with_invalid_data(topic_fixture: Topic) -> None:
        """Test topic form with valid data."""
        data = {"name": topic_fixture.name}
        form = TopicForm(data=data)
        assert form.is_valid() is False
        assert form.errors == {"name": ["Topic with this Name already exists."]}
