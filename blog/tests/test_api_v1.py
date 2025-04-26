import json
from http import HTTPStatus

import pytest
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse_lazy

from authentication.models import User
from blog.api.api_v1 import NO_PERMISSION
from blog.models import BlogPost, Topic

pytestmark = pytest.mark.django_db


class TestTopicList:
    """Tests topic list API."""

    @staticmethod
    def test_topic_list_with_bad_credentials(client: Client) -> None:
        """Test top list api with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_list")
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_topic_list(
        client: Client, topic_fixture: Topic, topic_fixture2: Topic, user_fixture: User
    ) -> None:
        """Test topic list API."""
        url = reverse_lazy("api-1.0.0:topic_list")
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        expected = {
            "items": [
                {
                    "id": topic_fixture.pk,
                    "name": topic_fixture.name,
                    "parent_topic": topic_fixture.parent_topic,
                },
                {
                    "id": topic_fixture2.pk,
                    "name": topic_fixture2.name,
                    "parent_topic": f"{topic_fixture2.parent_topic}",
                },
            ],
            "count": 2,
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected

    @staticmethod
    def test_topic_list_sort(
        client: Client, topic_fixture: Topic, topic_fixture2: Topic, user_fixture: User
    ) -> None:
        """Test topic list API with sort query parameter."""
        url = reverse_lazy("api-1.0.0:topic_list")
        response = client.get(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            query_params={"sort": "name"},
        )
        expected = {
            "items": [
                {
                    "id": topic_fixture2.pk,
                    "name": topic_fixture2.name,
                    "parent_topic": f"{topic_fixture2.parent_topic}",
                },
                {
                    "id": topic_fixture.pk,
                    "name": topic_fixture.name,
                    "parent_topic": topic_fixture.parent_topic,
                },
            ],
            "count": 2,
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected


class TestTopicDetail:
    """Tests for topic detail API."""

    @staticmethod
    def test_detail_with_bad_credentials(client: Client, topic_fixture: Topic) -> None:
        """Test detail api with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_detail", args=[topic_fixture.pk])
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_detail_api(
        client: Client, topic_fixture: Topic, user_fixture: User
    ) -> None:
        """Test topic detail API."""
        url = reverse_lazy("api-1.0.0:topic_detail", args=[topic_fixture.pk])
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        expected = {
            "id": topic_fixture.pk,
            "name": topic_fixture.name,
            "parent_topic": topic_fixture.parent_topic,
        }

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected


class TestCreateTopic:
    """Test create topic API."""

    @staticmethod
    def test_topic_create_with_bad_credentials(client: Client) -> None:
        """Test topic create api API with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_create")
        response = client.post(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_topic_create(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test create topic API."""
        url = reverse_lazy("api-1.0.0:topic_create")
        permission = Permission.objects.get(name="Can add topic")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {"name": "unittest", "parent_topic": topic_fixture.pk}
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        created = Topic.objects.get(name=data["name"])
        excpected = {
            "id": created.pk,
            "name": data["name"],
            "parent_topic": topic_fixture.name,
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == excpected

    @staticmethod
    def test_topic_create_with_no_permission(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test topic create API without no permission."""
        url = reverse_lazy("api-1.0.0:topic_create")
        data = {"name": "unittest", "parent_topic": topic_fixture.pk}
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}

    @staticmethod
    @pytest.mark.parametrize("field", ["name", "parent_topic"])
    def test_topic_create_missing_field(
        field: str, client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test create topic API with missing field."""
        url = reverse_lazy("api-1.0.0:topic_create")
        permission = Permission.objects.get(name="Can add topic")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {"name": "unittest", "parent_topic": topic_fixture.pk}
        del data[field]
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "payload", field],
                    "msg": "Field required",
                }
            ]
        }


class TestTopicUpdate:
    """Tests for topic update API."""

    @staticmethod
    def test_topic_update_with_bad_credentials(
        client: Client, topic_fixture: Topic
    ) -> None:
        """Test topic update API with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_update", args=[topic_fixture.pk])
        response = client.put(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_topic_update(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test topic update API."""
        url = reverse_lazy("api-1.0.0:topic_update", args=[topic_fixture.pk])
        permission = Permission.objects.get(name="Can change topic")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {"name": "unittest2", "parent_topic": None}
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        excpected = {
            "id": topic_fixture.pk,
            "name": data["name"],
            "parent_topic": data["parent_topic"],
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == excpected

    @staticmethod
    def test_topic_update_without_permission(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test topic update API without permission."""
        url = reverse_lazy("api-1.0.0:topic_update", args=[topic_fixture.pk])
        data = {"name": "unittest2", "parent_topic": None}
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}

    @staticmethod
    @pytest.mark.parametrize("field", ["name", "parent_topic"])
    def test_topic_update_with_missing_field(
        field: str, client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test topic update API with missing field."""
        url = reverse_lazy("api-1.0.0:topic_update", args=[topic_fixture.pk])
        data = {"name": "unittest2", "parent_topic": None}
        del data[field]
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "payload", field],
                    "msg": "Field required",
                }
            ]
        }


class TestTopicPartialUpdate:
    """Tests for topic partial update API."""

    @staticmethod
    def test_topic_partial_update_with_bad_credentials(
        client: Client, topic_fixture: Topic
    ) -> None:
        """Test topic partial update API with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_patch", args=[topic_fixture.pk])
        response = client.patch(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_topic_partial_update(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test topic partial update API."""
        url = reverse_lazy("api-1.0.0:topic_patch", args=[topic_fixture.pk])
        permission = Permission.objects.get(name="Can change topic")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {"name": "unittest2", "parent_topic": None}
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        excpected = {
            "id": topic_fixture.pk,
            "name": data["name"],
            "parent_topic": data["parent_topic"],
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == excpected

    @staticmethod
    def test_topic_partial_update_without_permission(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test topic partial update API without permission."""
        url = reverse_lazy("api-1.0.0:topic_patch", args=[topic_fixture.pk])
        data = {"name": "unittest2", "parent_topic": None}
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}

    @staticmethod
    @pytest.mark.parametrize("field", ["name", "parent_topic"])
    def test_topic_partial_update_with_missing_field(
        field: str, client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test topic partial update API with missing field."""
        permission = Permission.objects.get(name="Can change topic")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        url = reverse_lazy("api-1.0.0:topic_patch", args=[topic_fixture.pk])
        data = {"name": "unittest2", "parent_topic": None}
        del data[field]
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.OK


class TestTopicDelete:
    """Tests for topic delete API."""

    @staticmethod
    def test_topic_delete_with_bad_credentials(
        client: Client, topic_fixture: Topic
    ) -> None:
        """Test topic delete API with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_detail", args=[topic_fixture.pk])
        response = client.delete(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_topic_delete(
        client: Client, topic_fixture: Topic, user_fixture: User
    ) -> None:
        """Test topic delete API."""
        assert Topic.objects.exists() is True
        permission = Permission.objects.get(name="Can delete topic")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        url = reverse_lazy("api-1.0.0:topic_delete", args=[topic_fixture.pk])
        response = client.delete(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        assert response.status_code == HTTPStatus.OK
        assert Topic.objects.exists() is False

    @staticmethod
    def test_topic_delete_without_permission(
        client: Client, topic_fixture: Topic, user_fixture: User
    ) -> None:
        """Test topic delete API without permission."""
        url = reverse_lazy("api-1.0.0:topic_delete", args=[topic_fixture.pk])
        response = client.delete(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}


class TestBlogPostList:
    """Tests blog post list API."""

    @staticmethod
    def test_blog_post_list_with_bad_credentials(client: Client) -> None:
        """Test blog post list api with bad credentials."""
        url = reverse_lazy("api-1.0.0:blog_post_list")
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_blog_post_list(
        client: Client,
        blog_post_fixture: BlogPost,
        blog_post_fixture2: BlogPost,
        user_fixture: User,
    ) -> None:
        """Test blog post list API."""
        url = reverse_lazy("api-1.0.0:blog_post_list")
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        expected = {
            "items": [
                {
                    "id": blog_post_fixture.pk,
                    "title": blog_post_fixture.title,
                    "topic": blog_post_fixture.topic.name,
                    "author": blog_post_fixture.author.email,
                    "content": blog_post_fixture.content,
                    "created_at": blog_post_fixture.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )[:-4]
                    + "Z",
                    "previous": blog_post_fixture.previous.title
                    if blog_post_fixture.previous
                    else None,
                },
                {
                    "id": blog_post_fixture2.pk,
                    "title": blog_post_fixture2.title,
                    "topic": blog_post_fixture2.topic.name,
                    "author": blog_post_fixture2.author.email,
                    "content": blog_post_fixture2.content,
                    "created_at": blog_post_fixture2.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )[:-4]
                    + "Z",
                    "previous": blog_post_fixture2.previous.title
                    if blog_post_fixture2.previous
                    else None,
                },
            ],
            "count": 2,
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected

    @staticmethod
    def test_topic_list_sort(
        client: Client,
        blog_post_fixture: BlogPost,
        blog_post_fixture2: BlogPost,
        user_fixture: User,
    ) -> None:
        """Test blog post list API with sort query parameter."""
        url = reverse_lazy("api-1.0.0:blog_post_list")
        response = client.get(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            query_params={"sort": "title"},
        )
        expected = {
            "items": [
                {
                    "id": blog_post_fixture2.pk,
                    "title": blog_post_fixture2.title,
                    "topic": blog_post_fixture2.topic.name,
                    "author": blog_post_fixture2.author.email,
                    "content": blog_post_fixture2.content,
                    "created_at": blog_post_fixture2.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )[:-4]
                    + "Z",
                    "previous": blog_post_fixture2.previous.title
                    if blog_post_fixture2.previous
                    else None,
                },
                {
                    "id": blog_post_fixture.pk,
                    "title": blog_post_fixture.title,
                    "topic": blog_post_fixture.topic.name,
                    "author": blog_post_fixture.author.email,
                    "content": blog_post_fixture.content,
                    "created_at": blog_post_fixture.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )[:-4]
                    + "Z",
                    "previous": blog_post_fixture.previous.title
                    if blog_post_fixture.previous
                    else None,
                },
            ],
            "count": 2,
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected


class TestBlogPostDetail:
    """Tests for blog post detail API."""

    @staticmethod
    def test_blog_post_detail_with_bad_credentials(
        client: Client, blog_post_fixture: BlogPost
    ) -> None:
        """Test blog post detail api with bad credentials."""
        url = reverse_lazy("api-1.0.0:blog_post_detail", args=[blog_post_fixture.pk])
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_detail_api(
        client: Client, blog_post_fixture: BlogPost, user_fixture: User
    ) -> None:
        """Test blog post detail API."""
        url = reverse_lazy("api-1.0.0:blog_post_detail", args=[blog_post_fixture.pk])
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        expected = {
            "id": blog_post_fixture.pk,
            "title": blog_post_fixture.title,
            "topic": blog_post_fixture.topic.name,
            "author": blog_post_fixture.author.email,
            "content": blog_post_fixture.content,
            "created_at": blog_post_fixture.created_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )[:-4]
            + "Z",
            "previous": blog_post_fixture.previous.title
            if blog_post_fixture.previous
            else None,
        }

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected


class TestCreateBlogPost:
    """Test blog post create API."""

    @staticmethod
    def test_blog_post_create_with_bad_credentials(client: Client) -> None:
        """Test blog post create api API with bad credentials."""
        url = reverse_lazy("api-1.0.0:blog_post_create")
        response = client.post(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_blog_post_create(
        client: Client,
        user_fixture: User,
        topic_fixture: Topic,
        blog_post_fixture: BlogPost,
        image_upload_fixture: SimpleUploadedFile,
    ) -> None:
        """Test create blog post API."""
        url = reverse_lazy("api-1.0.0:blog_post_create")
        permission = Permission.objects.get(name="Can add blog post")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {
            "title": "foo",
            "topic": topic_fixture.pk,
            "content": "bar",
            "previous": blog_post_fixture.pk,
            "image": image_upload_fixture,
        }
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=data,
        )
        blog_post = BlogPost.objects.last()
        excpected = {
            "id": blog_post.pk,
            "title": data["title"],
            "topic": topic_fixture.name,
            "author": user_fixture.email,
            "content": data["content"],
            "created_at": blog_post.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]
            + "Z",
            "previous": blog_post_fixture.title,
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == excpected

    @staticmethod
    def test_blog_post_create_with_no_permission(
        client: Client,
        user_fixture: User,
        topic_fixture: Topic,
        blog_post_fixture: BlogPost,
        image_upload_fixture: SimpleUploadedFile,
    ) -> None:
        """Test blog post create API without no permission."""
        url = reverse_lazy("api-1.0.0:blog_post_create")
        data = {
            "title": "foo",
            "topic": topic_fixture.pk,
            "content": "bar",
            "previous": blog_post_fixture.pk,
            "image": image_upload_fixture,
        }
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=data,
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}

    @staticmethod
    @pytest.mark.parametrize("field", ["title", "topic", "content", "previous"])
    def test_blog_post_create_missing_field(  # noqa: PLR0913
        field: str,
        client: Client,
        user_fixture: User,
        topic_fixture: Topic,
        blog_post_fixture: BlogPost,
        image_upload_fixture: SimpleUploadedFile,
    ) -> None:
        """Test create blog post API with missing field."""
        url = reverse_lazy("api-1.0.0:blog_post_create")
        permission = Permission.objects.get(name="Can add blog post")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {
            "title": "foo",
            "topic": topic_fixture.pk,
            "content": "bar",
            "previous": blog_post_fixture.pk,
            "image": image_upload_fixture,
        }
        del data[field]
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=data,
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["form", field],
                    "msg": "Field required",
                }
            ]
        }


class TestUpdateBlogPost:
    """Test blog post update API."""

    @staticmethod
    def test_blog_post_update_with_bad_credentials(
        client: Client, blog_post_fixture: BlogPost
    ) -> None:
        """Test blog post update api API with bad credentials."""
        url = reverse_lazy("api-1.0.0:blog_post_update", args=[blog_post_fixture.pk])
        response = client.put(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_blog_post_update(
        client: Client,
        user_fixture: User,
        blog_post_fixture: BlogPost,
    ) -> None:
        """Test update blog post API."""
        url = reverse_lazy("api-1.0.0:blog_post_update", args=[blog_post_fixture.pk])
        permission = Permission.objects.get(name="Can change blog post")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {
            "title": "foo",
            "topic": blog_post_fixture.topic.pk,
            "content": "bar",
            "previous": blog_post_fixture.pk,
        }
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        excpected = {
            "id": blog_post_fixture.pk,
            "title": data["title"],
            "topic": blog_post_fixture.topic.name,
            "author": user_fixture.email,
            "content": data["content"],
            "created_at": blog_post_fixture.created_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )[:-4]
            + "Z",
            "previous": blog_post_fixture.title,
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == excpected

    @staticmethod
    def test_blog_post_update_with_no_permission(
        client: Client,
        user_fixture: User,
        blog_post_fixture: BlogPost,
    ) -> None:
        """Test blog post update API without no permission."""
        url = reverse_lazy("api-1.0.0:blog_post_update", args=[blog_post_fixture.pk])
        data = {
            "title": "foo",
            "topic": blog_post_fixture.topic.pk,
            "content": "bar",
            "previous": blog_post_fixture.pk,
        }
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}

    @staticmethod
    @pytest.mark.parametrize("field", ["title", "topic", "content", "previous"])
    def test_blog_post_update_missing_field(
        field: str, client: Client, user_fixture: User, blog_post_fixture: BlogPost
    ) -> None:
        """Test blog post update API with missing field."""
        url = reverse_lazy("api-1.0.0:blog_post_update", args=[blog_post_fixture.pk])
        permission = Permission.objects.get(name="Can change blog post")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {
            "title": "foo",
            "topic": blog_post_fixture.topic.pk,
            "content": "bar",
            "previous": None,
        }
        del data[field]
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "payload", field],
                    "msg": "Field required",
                }
            ]
        }


class TestPatialUpdateBlogPost:
    """Test blog post partial update API."""

    @staticmethod
    def test_blog_post_partial_update_with_bad_credentials(
        client: Client, blog_post_fixture: BlogPost
    ) -> None:
        """Test blog post partial update api API with bad credentials."""
        url = reverse_lazy("api-1.0.0:blog_post_patch", args=[blog_post_fixture.pk])
        response = client.patch(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_blog_post_partial_update(
        client: Client,
        user_fixture: User,
        blog_post_fixture: BlogPost,
    ) -> None:
        """Test blog post partial update API."""
        url = reverse_lazy("api-1.0.0:blog_post_patch", args=[blog_post_fixture.pk])
        permission = Permission.objects.get(name="Can change blog post")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        data = {"title": "foo"}
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        blog_post_fixture.refresh_from_db()
        excpected = {
            "id": blog_post_fixture.pk,
            "title": data["title"],
            "topic": blog_post_fixture.topic.name,
            "author": user_fixture.email,
            "content": blog_post_fixture.content,
            "created_at": blog_post_fixture.created_at.strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )[:-4]
            + "Z",
            "previous": None,
        }
        assert blog_post_fixture.title == data["title"]
        assert response.status_code == HTTPStatus.OK
        assert response.json() == excpected

    @staticmethod
    def test_blog_post_partial_update_with_no_permission(
        client: Client,
        user_fixture: User,
        blog_post_fixture: BlogPost,
    ) -> None:
        """Test blog post partial update API without no permission."""
        url = reverse_lazy("api-1.0.0:blog_post_patch", args=[blog_post_fixture.pk])
        data = {"title": "foo"}
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}

class TestBlogPostDelete:
    """Tests for blog post delete API."""

    @staticmethod
    def test_blog_post_delete_with_bad_credentials(
        client: Client, blog_post_fixture: BlogPost
    ) -> None:
        """Test blog post delete API with bad credentials."""
        url = reverse_lazy("api-1.0.0:blog_post_delete", args=[blog_post_fixture.pk])
        response = client.delete(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_blog_post_delete(
        client: Client, blog_post_fixture: BlogPost, user_fixture: User
    ) -> None:
        """Test blog post delete API."""
        assert BlogPost.objects.exists() is True
        permission = Permission.objects.get(name="Can delete blog post")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        url = reverse_lazy("api-1.0.0:blog_post_delete", args=[blog_post_fixture.pk])
        response = client.delete(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert BlogPost.objects.exists() is False

    @staticmethod
    def test_blog_post_delete_without_permission(
        client: Client, blog_post_fixture: BlogPost, user_fixture: User
    ) -> None:
        """Test blog post delete API without permission."""
        url = reverse_lazy("api-1.0.0:blog_post_delete", args=[blog_post_fixture.pk])
        response = client.delete(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}
