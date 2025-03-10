import pytest
from django.db.utils import IntegrityError

from blog.models import Topic

pytestmark = pytest.mark.django_db


class TestTopicModel:
    """Test topic model."""

    @staticmethod
    def test_create_topic() -> None:
        """Test create Topic."""
        topic = Topic(name="test")
        topic.save()
        assert len(Topic.objects.all()) == 1
        assert Topic.objects.all()[0] == topic

    @staticmethod
    def test_name_is_unique(topic_fixture: Topic) -> None:
        """Test topic name is unique."""
        topic = Topic(name=topic_fixture.name)
        with pytest.raises(IntegrityError):
            topic.save()
