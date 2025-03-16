import pytest

from authentication.models import User
from blog.forms import PostForm, TopicForm
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


class TestPostForm:
    """Test post form."""

    @staticmethod
    def test_post_form(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post form with valid data."""
        data = {
            "title": "Title",
            "author": user_fixture,
            "topic": topic_fixture,
            "content": "Content",
        }
        form = PostForm(data=data)
        assert form.is_valid() is True

    @staticmethod
    @pytest.mark.parametrize("field", ["title", "content"])
    def test_post_form_with_missing_data(
        field: str, topic_fixture: Topic, user_fixture: User
    ) -> None:
        """Test post form with missing required field."""
        data = {
            "title": "Title",
            "author": user_fixture,
            "topic": topic_fixture,
            "content": "Content",
        }
        del data[field]
        form = PostForm(data=data)
        assert form.is_valid() is False
        assert form.errors[field] == ["This field is required."]
