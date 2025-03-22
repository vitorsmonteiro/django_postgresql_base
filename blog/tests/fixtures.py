import pytest

from authentication.models import User
from blog.models import Post, Topic

pytestmark = pytest.mark.django_db


@pytest.fixture
def topic_fixture() -> Topic:
    """Topic fixtrue."""
    topic = Topic(name="test")
    topic.save()
    return topic


@pytest.fixture
def topic_fixture2() -> Topic:
    """Topic fixtrue 2."""
    topic = Topic(name="another_test")
    topic.save()
    return topic

@pytest.fixture
def post_fixture(topic_fixture: Topic, user_fixture: User) -> Post:
    """Post fixture."""
    post = Post(
        title="Test", topic=topic_fixture, author=user_fixture, content="content"
    )
    post.save()
    return post
