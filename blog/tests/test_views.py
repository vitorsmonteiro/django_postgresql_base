from http import HTTPStatus

import pytest
from django.contrib.auth.models import AnonymousUser, Permission
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse_lazy

from authentication.models import User
from blog.models import BlogPost, Topic
from blog.views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    TopicCreateView,
    TopicDeleteView,
    TopicListView,
    TopicUpdateView,
)

pytestmark = pytest.mark.django_db
request_factory = RequestFactory()


class TestTopicListView:
    """Tests for Topic List View."""

    @staticmethod
    def test_view_normal(topic_fixture: Topic, user_fixture: User) -> None:
        """Test view from normal request."""
        url = reverse_lazy("blog:topic_list")
        request = request_factory.get(url)
        request.user = user_fixture
        response = TopicListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/topic_list.html"
        assert topic_fixture in response.context_data["object_list"]

    @staticmethod
    def test_view_htmx(
        topic_fixture: Topic,  # noqa: ARG004
        topic_fixture2: Topic,  # noqa: ARG004
        user_fixture: User,
    ) -> None:
        """Test view from HTMX."""
        url = reverse_lazy("blog:topic_list")
        request = request_factory.get(url, headers={"Hx-Request": "true"})
        request.user = user_fixture
        response = TopicListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/components/topic_table.html"
        assert list(response.context_data["object_list"]) == list(
            Topic.objects.all().order_by("name")
        )

    @staticmethod
    def test_view_htmx_search(
        topic_fixture: Topic,  # noqa: ARG004
        topic_fixture2: Topic,  # noqa: ARG004
        user_fixture: User,
    ) -> None:
        """Test view from HTMX."""
        url = reverse_lazy("blog:topic_list")
        request = request_factory.get(
            url, headers={"Hx-Request": "true"}, query_params={"search": "tes"}
        )
        request.user = user_fixture
        response = TopicListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/components/topic_table.html"
        assert list(response.context_data["object_list"]) == list(
            Topic.objects.filter(name__startswith="tes")
        )

    @staticmethod
    def test_view_not_logged() -> None:
        """Test view user not logged."""
        url = reverse_lazy("blog:topic_list")
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = TopicListView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/blog/topic_list"


class TestTopicDeleteView:
    """Tests for topic delete view."""

    @staticmethod
    def test_get_view_not_logged(topic_fixture: Topic) -> None:
        """Test get delete view without loggin."""
        url = reverse_lazy("blog:topic_delete", args=[topic_fixture.pk])
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = TopicDeleteView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/topic_delete/{topic_fixture.pk}"

    @staticmethod
    def test_get_view_forbidden(topic_fixture: Topic, user_fixture: User) -> None:
        """Test get delete view logged in."""
        url = reverse_lazy("blog:topic_delete", args=[topic_fixture.pk])
        request = request_factory.get(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            TopicDeleteView.as_view()(request, pk=topic_fixture.pk)

    @staticmethod
    def test_get_view(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post view ok."""
        url = reverse_lazy("blog:topic_delete", args=[topic_fixture.pk])
        request = request_factory.get(url)
        delete_permission = Permission.objects.get(
            codename="delete_topic", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(delete_permission)
        request.user = user_fixture
        response = TopicDeleteView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == ["blog/topic_confirm_delete.html"]

    @staticmethod
    def test_blogpost_view_not_logged(topic_fixture: Topic) -> None:
        """Test post delete view without loggin."""
        url = reverse_lazy("blog:topic_delete", args=[topic_fixture.pk])
        request = request_factory.post(url)
        request.user = AnonymousUser()
        response = TopicDeleteView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/topic_delete/{topic_fixture.pk}"

    @staticmethod
    def test_blogpost_view_forbidden(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post delete view logged in."""
        url = reverse_lazy("blog:topic_delete", args=[topic_fixture.pk])
        request = request_factory.post(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            TopicDeleteView.as_view()(request, pk=topic_fixture.pk)

    @staticmethod
    def test_blogpost_view(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post delete view ok."""
        url = reverse_lazy("blog:topic_delete", args=[topic_fixture.pk])
        request = request_factory.delete(url)
        delete_permission = Permission.objects.get(
            codename="delete_topic", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(delete_permission)
        request.user = user_fixture
        response = TopicDeleteView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse_lazy("blog:topic_list")
        assert Topic.objects.filter(pk=topic_fixture.pk).exists() is False


class TestTopicCreateView:
    """Tests for Topic Create View."""

    @staticmethod
    def test_get_view_not_logged() -> None:
        """Test get create view without logging in."""
        url = reverse_lazy("blog:topic_create")
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = TopicCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/blog/topic_create"

    @staticmethod
    def test_get_view_forbidden(user_fixture: User) -> None:
        """Test get create view logged in without permission."""
        url = reverse_lazy("blog:topic_create")
        request = request_factory.get(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            TopicCreateView.as_view()(request)

    @staticmethod
    def test_get_view(user_fixture: User) -> None:
        """Test get create view with permission."""
        url = reverse_lazy("blog:topic_create")
        request = request_factory.get(url)
        add_permission = Permission.objects.get(
            codename="add_topic", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(add_permission)
        request.user = user_fixture
        response = TopicCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == ["blog/topic_create.html"]

    @staticmethod
    def test_blogpost_view_not_logged() -> None:
        """Test post create view without logging in."""
        url = reverse_lazy("blog:topic_create")
        request = request_factory.post(url, data={"name": "Test Topic"})
        request.user = AnonymousUser()
        response = TopicCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/blog/topic_create"

    @staticmethod
    def test_blogpost_view_forbidden(user_fixture: User) -> None:
        """Test post create view logged in without permission."""
        url = reverse_lazy("blog:topic_create")
        request = request_factory.post(url, data={"name": "Test Topic"})
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            TopicCreateView.as_view()(request)

    @staticmethod
    def test_blogpost_view(user_fixture: User) -> None:
        """Test post create view with permission."""
        url = reverse_lazy("blog:topic_create")
        request = request_factory.post(url, data={"name": "Test Topic"})
        add_permission = Permission.objects.get(
            codename="add_topic", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(add_permission)
        request.user = user_fixture
        response = TopicCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse_lazy("blog:topic_list")
        assert Topic.objects.filter(name="Test Topic").exists() is True


class TestTopicUpdateView:
    """Tests for Topic Update View."""

    @staticmethod
    def test_get_view_not_logged(topic_fixture: Topic) -> None:
        """Test get update view without logging in."""
        url = reverse_lazy("blog:topic_update", args=[topic_fixture.pk])
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = TopicUpdateView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/topic_update/{topic_fixture.pk}"

    @staticmethod
    def test_get_view_forbidden(topic_fixture: Topic, user_fixture: User) -> None:
        """Test get update view logged in without permission."""
        url = reverse_lazy("blog:topic_update", args=[topic_fixture.pk])
        request = request_factory.get(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            TopicUpdateView.as_view()(request, pk=topic_fixture.pk)

    @staticmethod
    def test_get_view(topic_fixture: Topic, user_fixture: User) -> None:
        """Test get update view with permission."""
        url = reverse_lazy("blog:topic_update", args=[topic_fixture.pk])
        request = request_factory.get(url)
        change_permission = Permission.objects.get(
            codename="change_topic", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(change_permission)
        request.user = user_fixture
        response = TopicUpdateView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == ["blog/topic_update.html"]
        assert response.context_data["topic"] == topic_fixture

    @staticmethod
    def test_blogpost_view_not_logged(topic_fixture: Topic) -> None:
        """Test post update view without logging in."""
        url = reverse_lazy("blog:topic_update", args=[topic_fixture.pk])
        request = request_factory.post(url, data={"name": "Updated Topic"})
        request.user = AnonymousUser()
        response = TopicUpdateView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/topic_update/{topic_fixture.pk}"

    @staticmethod
    def test_blogpost_view_forbidden(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post update view logged in without permission."""
        url = reverse_lazy("blog:topic_update", args=[topic_fixture.pk])
        request = request_factory.post(url, data={"name": "Updated Topic"})
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            TopicUpdateView.as_view()(request, pk=topic_fixture.pk)

    @staticmethod
    def test_blogpost_view(topic_fixture: Topic, user_fixture: User) -> None:
        """Test post update view with permission."""
        url = reverse_lazy("blog:topic_update", args=[topic_fixture.pk])
        request = request_factory.post(url, data={"name": "Updated Topic"})
        change_permission = Permission.objects.get(
            codename="change_topic", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(change_permission)
        request.user = user_fixture
        response = TopicUpdateView.as_view()(request, pk=topic_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse_lazy("blog:topic_list")
        topic_fixture.refresh_from_db()
        assert topic_fixture.name == "Updated Topic"


class TestBlogListView:
    """Tests for Post List View."""

    @staticmethod
    def test_view_normal(post_fixture: BlogPost, user_fixture: User) -> None:
        """Test view from normal request."""
        url = reverse_lazy("blog:post_list")
        request = request_factory.get(url)
        request.user = user_fixture
        response = PostListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/post_list.html"
        assert post_fixture in response.context_data["object_list"]

    @staticmethod
    def test_view_htmx(
        post_fixture: BlogPost,  # noqa: ARG004
        post_fixture2: BlogPost,  # noqa: ARG004
        user_fixture: User,
    ) -> None:
        """Test view from HTMX."""
        url = reverse_lazy("blog:post_list")
        request = request_factory.get(url, headers={"Hx-Request": "true"})
        request.user = user_fixture
        response = PostListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/components/post_table.html"
        assert list(response.context_data["object_list"]) == list(
            BlogPost.objects.all().order_by("title")
        )

    @staticmethod
    def test_view_htmx_search(
        post_fixture: BlogPost,  # noqa: ARG004
        post_fixture2: BlogPost,  # noqa: ARG004
        user_fixture: User,
    ) -> None:
        """Test view from HTMX with search."""
        url = reverse_lazy("blog:post_list")
        request = request_factory.get(
            url, headers={"Hx-Request": "true"}, query_params={"search": "tes"}
        )
        request.user = user_fixture
        response = PostListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/components/post_table.html"
        assert list(response.context_data["object_list"]) == list(
            BlogPost.objects.filter(title__startswith="tes")
        )

    @staticmethod
    def test_view_not_logged() -> None:
        """Test view user not logged."""
        url = reverse_lazy("blog:post_list")
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = PostListView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/blog/post_list"


class TestBlogCreateView:
    """Tests for Post Create View."""

    @staticmethod
    def test_get_view_not_logged() -> None:
        """Test get create view without logging in."""
        url = reverse_lazy("blog:post_create")
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = PostCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/blog/post_create"

    @staticmethod
    def test_get_view_forbidden(user_fixture: User) -> None:
        """Test get create view logged in without permission."""
        url = reverse_lazy("blog:post_create")
        request = request_factory.get(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            PostCreateView.as_view()(request)

    @staticmethod
    def test_get_view(user_fixture: User) -> None:
        """Test get create view with permission."""
        url = reverse_lazy("blog:post_create")
        request = request_factory.get(url)
        add_permission = Permission.objects.get(
            codename="add_blogpost", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(add_permission)
        request.user = user_fixture
        response = PostCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == ["blog/post_create.html"]
        assert "topics" in response.context_data
        assert "posts" in response.context_data

    @staticmethod
    def test_blogpost_view_not_logged() -> None:
        """Test post create view without logging in."""
        url = reverse_lazy("blog:post_create")
        request = request_factory.post(
            url, data={"title": "Test Post", "content": "Test Content"}
        )
        request.user = AnonymousUser()
        response = PostCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/blog/post_create"

    @staticmethod
    def test_blogpost_view_forbidden(user_fixture: User) -> None:
        """Test post create view logged in without permission."""
        url = reverse_lazy("blog:post_create")
        request = request_factory.post(
            url, data={"title": "Test Post", "content": "Test Content"}
        )
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            PostCreateView.as_view()(request)

    @staticmethod
    def test_blogpost_view(user_fixture: User, topic_fixture: Topic) -> None:
        """Test post create view with permission."""
        url = reverse_lazy("blog:post_create")
        request = request_factory.post(
            url,
            data={
                "title": "Test Post",
                "content": "Test Content",
                "topic": topic_fixture.pk,
            },
        )
        add_permission = Permission.objects.get(
            codename="add_blogpost", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(add_permission)
        request.user = user_fixture
        response = PostCreateView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse_lazy("blog:post_list")
        assert BlogPost.objects.filter(title="Test Post").exists() is True


class TestBlogUpdateView:
    """Tests for Post Update View."""

    @staticmethod
    def test_get_view_not_logged(post_fixture: BlogPost) -> None:
        """Test get update view without logging in."""
        url = reverse_lazy("blog:post_update", args=[post_fixture.pk])
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = PostUpdateView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/post_update/{post_fixture.pk}"

    @staticmethod
    def test_get_view_forbidden(post_fixture: BlogPost, user_fixture: User) -> None:
        """Test get update view logged in without permission."""
        url = reverse_lazy("blog:post_update", args=[post_fixture.pk])
        request = request_factory.get(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            PostUpdateView.as_view()(request, pk=post_fixture.pk)

    @staticmethod
    def test_get_view(post_fixture: BlogPost, user_fixture: User) -> None:
        """Test get update view with permission."""
        url = reverse_lazy("blog:post_update", args=[post_fixture.pk])
        request = request_factory.get(url)
        change_permission = Permission.objects.get(
            codename="change_blogpost", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(change_permission)
        request.user = user_fixture
        response = PostUpdateView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == ["blog/post_update.html"]
        assert response.context_data["post"] == post_fixture
        assert "topics" in response.context_data
        assert "posts" in response.context_data

    @staticmethod
    def test_blogpost_view_not_logged(post_fixture: BlogPost) -> None:
        """Test post update view without logging in."""
        url = reverse_lazy("blog:post_update", args=[post_fixture.pk])
        request = request_factory.post(
            url, data={"title": "Updated Post", "content": "Updated Content"}
        )
        request.user = AnonymousUser()
        response = PostUpdateView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/post_update/{post_fixture.pk}"

    @staticmethod
    def test_blogpost_view_forbidden(
        post_fixture: BlogPost, user_fixture: User
    ) -> None:
        """Test post update view logged in without permission."""
        url = reverse_lazy("blog:post_update", args=[post_fixture.pk])
        request = request_factory.post(
            url, data={"title": "Updated Post", "content": "Updated Content"}
        )
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            PostUpdateView.as_view()(request, pk=post_fixture.pk)

    @staticmethod
    def test_blogpost_view(
        post_fixture: BlogPost, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test post update view with permission."""
        url = reverse_lazy("blog:post_update", args=[post_fixture.pk])
        data = {
            "title": "Updated Post",
            "content": "Updated Content",
            "topic": topic_fixture.pk,
        }
        request = request_factory.post(url, data=data)
        change_permission = Permission.objects.get(
            codename="change_blogpost", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(change_permission)
        request.user = user_fixture
        response = PostUpdateView.as_view()(request, pk=post_fixture.pk)
        post_fixture.refresh_from_db()
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse_lazy("blog:post_list")
        assert post_fixture.title == "Updated Post"
        assert post_fixture.content == "Updated Content"
        assert post_fixture.topic == topic_fixture


class TestBlogPostDetailView:
    """Tests for Post Detail View."""

    @staticmethod
    def test_get_view(post_fixture: BlogPost) -> None:
        """Test detail view with logged-in user."""
        url = reverse_lazy("blog:post_detail", args=[post_fixture.pk])
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = PostDetailView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == ["blog/post_detail.html"]
        assert response.context_data["post"] == post_fixture


class TestBlogPostDeleteView:
    """Tests for Post Delete View."""

    @staticmethod
    def test_get_view_not_logged(post_fixture: BlogPost) -> None:
        """Test get delete view without logging in."""
        url = reverse_lazy("blog:post_delete", args=[post_fixture.pk])
        request = request_factory.get(url)
        request.user = AnonymousUser()
        response = PostDeleteView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/post_delete/{post_fixture.pk}"

    @staticmethod
    def test_get_view_forbidden(post_fixture: BlogPost, user_fixture: User) -> None:
        """Test get delete view logged in without permission."""
        url = reverse_lazy("blog:post_delete", args=[post_fixture.pk])
        request = request_factory.get(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            PostDeleteView.as_view()(request, pk=post_fixture.pk)

    @staticmethod
    def test_get_view(post_fixture: BlogPost, user_fixture: User) -> None:
        """Test get delete view with permission."""
        url = reverse_lazy("blog:post_delete", args=[post_fixture.pk])
        request = request_factory.get(url)
        delete_permission = Permission.objects.get(
            codename="delete_blogpost", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(delete_permission)
        request.user = user_fixture
        response = PostDeleteView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == ["blog/post_confirm_delete.html"]
        assert response.context_data["post"] == post_fixture

    @staticmethod
    def test_post_view_not_logged(post_fixture: BlogPost) -> None:
        """Test post delete view without logging in."""
        url = reverse_lazy("blog:post_delete", args=[post_fixture.pk])
        request = request_factory.post(url)
        request.user = AnonymousUser()
        response = PostDeleteView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"/login?next=/blog/post_delete/{post_fixture.pk}"

    @staticmethod
    def test_post_view_forbidden(post_fixture: BlogPost, user_fixture: User) -> None:
        """Test post delete view logged in without permission."""
        url = reverse_lazy("blog:post_delete", args=[post_fixture.pk])
        request = request_factory.post(url)
        request.user = user_fixture
        with pytest.raises(PermissionDenied):
            PostDeleteView.as_view()(request, pk=post_fixture.pk)

    @staticmethod
    def test_post_view(post_fixture: BlogPost, user_fixture: User) -> None:
        """Test post delete view with permission."""
        url = reverse_lazy("blog:post_delete", args=[post_fixture.pk])
        request = request_factory.post(url)
        delete_permission = Permission.objects.get(
            codename="delete_blogpost", content_type__app_label="blog"
        )
        user_fixture.user_permissions.add(delete_permission)
        request.user = user_fixture
        response = PostDeleteView.as_view()(request, pk=post_fixture.pk)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse_lazy("blog:post_list")
        assert BlogPost.objects.filter(pk=post_fixture.pk).exists() is False
