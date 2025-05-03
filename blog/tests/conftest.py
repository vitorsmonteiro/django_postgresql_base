import pytest

from authentication.models import User
from blog.models import BlogPost, Comment, Topic

pytestmark = pytest.mark.django_db


@pytest.fixture
def topic_fixture() -> Topic:
    """Topic fixtrue."""
    return Topic.objects.create(name="test")


@pytest.fixture
def topic_fixture2(topic_fixture: Topic) -> Topic:
    """Topic fixtrue 2."""
    return Topic.objects.create(name="another_test", parent_topic=topic_fixture)


@pytest.fixture
def blog_post_fixture(topic_fixture: Topic, user_fixture: User) -> BlogPost:
    """Blog post fixture."""
    return BlogPost.objects.create(
        title="Test", topic=topic_fixture, author=user_fixture, content="content"
    )


@pytest.fixture
def blog_post_fixture2(topic_fixture2: Topic, user_fixture: User) -> BlogPost:
    """Blog post fixture 2."""
    return BlogPost.objects.create(
        title="Another test",
        topic=topic_fixture2,
        author=user_fixture,
        content="content2",
    )


@pytest.fixture
def comment_fixture(blog_post_fixture: BlogPost, user_fixture: User) -> Comment:
    """Comment fixture."""
    return Comment.objects.create(
        blog_post=blog_post_fixture, author=user_fixture, comment="test"
    )
