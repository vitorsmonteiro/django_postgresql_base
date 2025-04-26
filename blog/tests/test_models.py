import pytest
from django.db.utils import IntegrityError

from authentication.models import User
from blog.models import BlogPost, Topic

pytestmark = pytest.mark.django_db


class TestTopicModel:
    """Test topic model."""

    @staticmethod
    def test_create_topic() -> None:
        """Test create Topic."""
        assert Topic.objects.exists() is False
        topic = Topic.objects.create(name="test")
        assert Topic.objects.exists() is True
        assert Topic.objects.first() == topic

    @staticmethod
    def test_name_is_unique(topic_fixture: Topic) -> None:
        """Test topic name is unique."""
        topic = Topic(name=topic_fixture.name)
        with pytest.raises(IntegrityError):
            topic.save()


class TestPostModel:
    """Test post model."""

    @staticmethod
    def test_create_post(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post creation."""
        assert BlogPost.objects.exists() is False
        post = BlogPost(
            title="Test", topic=topic_fixture, author=user_fixture, content="content"
        )
        post.save()
        assert BlogPost.objects.exists() is True
        assert BlogPost.objects.first() == post
