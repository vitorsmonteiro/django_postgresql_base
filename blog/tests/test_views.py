from http import HTTPStatus

import pytest
from django.test import RequestFactory
from django.urls import reverse_lazy

from authentication.models import User
from blog.models import Post, Topic
from blog.views import TopicListView

pytestmark = pytest.mark.django_db
factory = RequestFactory()


class TestTopicListView:
    """Tests for Topic List View."""

    @staticmethod
    def test_get_view_normal(topic_fixture: Topic, user_fixture: User) -> None:
        """Test get view from normal request."""
        url = reverse_lazy("blog:topic_list")
        request = factory.get(url)
        request.user = user_fixture
        response = TopicListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/topic_list.html"
        assert topic_fixture in response.context_data["object_list"]

    @staticmethod
    def test_get_view_htmx(topic_fixture: Topic, user_fixture: User) -> None:
        """Test get view from HTMX."""
        url = reverse_lazy("blog:topic_list")
        request = factory.get(url, headers={"Hx-Request": "true"})
        request.user = user_fixture
        response = TopicListView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert response.template_name == "blog/components/topic_table.html"
        assert topic_fixture in response.context_data["object_list"]
