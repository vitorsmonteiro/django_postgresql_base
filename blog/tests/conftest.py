import pytest

from authentication.models import User
from blog.models import BlogPost, Topic

pytestmark = pytest.mark.django_db


@pytest.fixture
def topic_fixture() -> Topic:
    """Topic fixtrue."""
    topic = Topic(name="test")
    topic.save()
    return topic


@pytest.fixture
def topic_fixture2(topic_fixture: Topic) -> Topic:
    """Topic fixtrue 2."""
    topic = Topic(name="another_test", parent_topic=topic_fixture)
    topic.save()
    return topic


@pytest.fixture
def blog_post_fixture(topic_fixture: Topic, user_fixture: User) -> BlogPost:
    """Blog post fixture."""
    post = BlogPost(
        title="Test", topic=topic_fixture, author=user_fixture, content="content"
    )
    post.save()
    return post


@pytest.fixture
def blog_post_fixture2(topic_fixture2: Topic, user_fixture: User) -> BlogPost:
    """Blog post fixture 2."""
    post = BlogPost(
        title="Another test",
        topic=topic_fixture2,
        author=user_fixture,
        content="content2",
    )
    post.save()
    return post
