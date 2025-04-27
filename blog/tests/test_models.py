import pytest
from django.db.utils import IntegrityError

from authentication.models import User
from blog.models import BlogPost, Commment, Topic

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
        with pytest.raises(IntegrityError):
            Topic.objects.create(name=topic_fixture.name)

    @staticmethod
    def test_parent_topic_delete_set_none(
        topic_fixture: Topic, topic_fixture2: Topic
    ) -> None:
        """Test that when a parent topic is removed field is set to None."""
        assert topic_fixture2.parent_topic == topic_fixture
        topic_fixture.delete()
        topic_fixture2.refresh_from_db()
        assert topic_fixture2.parent_topic is None


class TestPostModel:
    """Test post model."""

    @staticmethod
    def test_create_post(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post creation."""
        assert BlogPost.objects.exists() is False
        post = BlogPost.objects.create(
            title="Test", topic=topic_fixture, author=user_fixture, content="content"
        )
        assert BlogPost.objects.exists() is True
        assert BlogPost.objects.first() == post

    @staticmethod
    def test_next_post(
        blog_post_fixture: BlogPost, blog_post_fixture2: BlogPost
    ) -> None:
        """Test next post."""
        blog_post_fixture2.previous = blog_post_fixture
        blog_post_fixture2.save()
        blog_post_fixture.refresh_from_db()
        assert blog_post_fixture.next == blog_post_fixture2

    @staticmethod
    def test_set_topic_null_when_topic_is_removed(
        blog_post_fixture: BlogPost, topic_fixture: Topic
    ) -> None:
        """Test that when a topic is removed field is set to None."""
        assert blog_post_fixture.topic == topic_fixture
        topic_fixture.delete()
        blog_post_fixture.refresh_from_db()
        assert blog_post_fixture.topic is None

    @staticmethod
    def test_set_author_null_when_autheor_is_removed(
        blog_post_fixture: BlogPost, user_fixture: User
    ) -> None:
        """Test that when a author is removed field is set to None."""
        assert blog_post_fixture.author == user_fixture
        user_fixture.delete()
        blog_post_fixture.refresh_from_db()
        assert blog_post_fixture.author is None

    @staticmethod
    def test_set_preovious_null_when_blog_post_is_removed(
        blog_post_fixture: BlogPost, blog_post_fixture2: BlogPost
    ) -> None:
        """Test that when a blog post is removed previous is set to None."""
        blog_post_fixture2.previous = blog_post_fixture
        blog_post_fixture2.save()
        assert blog_post_fixture2.previous == blog_post_fixture
        blog_post_fixture.delete()
        blog_post_fixture2.refresh_from_db()
        assert blog_post_fixture2.previous is None


class TestCommentModel:
    """Test comment model."""

    @staticmethod
    def test_comment_create(blog_post_fixture: BlogPost, user_fixture: User) -> None:
        """Test comment create."""
        assert Commment.objects.exists() is False
        comment = Commment.objects.create(
            blog_post=blog_post_fixture, author=user_fixture, comment="foo"
        )
        assert Commment.objects.exists() is True
        assert Commment.objects.first() == comment

    @staticmethod
    def test_comment_is_deleted_when_post_is_deleted(comment_fixture: Commment) -> None:
        """Test that a comment is deleted when a post is deleted."""
        assert Commment.objects.exists() is True
        comment_fixture.blog_post.delete()
        assert Commment.objects.exists() is False

    @staticmethod
    def test_comment_is_deleted_when_user_is_deleted(comment_fixture: Commment) -> None:
        """Test that a comment is deleted when a user is deleted."""
        assert Commment.objects.exists() is True
        comment_fixture.author.delete()
        assert Commment.objects.exists() is False
