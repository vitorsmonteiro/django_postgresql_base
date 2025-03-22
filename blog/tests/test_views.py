from http import HTTPStatus

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse_lazy

from authentication.models import User
from blog.models import Topic
from blog.views import TopicListView

pytestmark = pytest.mark.django_db
factory = RequestFactory()


class TestTopicListView:
    """Tests for Topic List View."""

    @staticmethod
    def test_view_normal(topic_fixture: Topic, user_fixture: User) -> None:
        """Test view from normal request."""
        url = reverse_lazy("blog:topic_list")
        request = factory.get(url)
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
        request = factory.get(url, headers={"Hx-Request": "true"})
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
        request = factory.get(
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
        request = factory.get(url)
        request.user = AnonymousUser()
        response = TopicListView.as_view()(request)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == "/login?next=/blog/topic_list"
