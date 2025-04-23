import json
from http import HTTPStatus

import pytest
from django.contrib.auth.models import Permission
from django.test import Client
from django.urls import reverse_lazy

from authentication.models import User
from blog.api.api_v1 import NO_PERMISSION
from blog.models import BlogPost, Topic

pytestmark = pytest.mark.django_db


class TestListTopic:
    """Test list topic API."""

    @staticmethod
    def test_list_with_bad_credentials(client: Client) -> None:
        """Test list api with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_list")
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_list_api(
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
    def test_list_api_sort(
        client: Client, topic_fixture: Topic, topic_fixture2: Topic, user_fixture: User
    ) -> None:
        """Test topic list API."""
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
    """Test topic detail API."""

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
    def test_create_with_bad_credentials(client: Client) -> None:
        """Test create api with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_create")
        response = client.post(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_create_api(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test create topic."""
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
    def test_create_api_with_no_permission(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test create topic API with user with no permission."""
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
    def test_create_api_missing_field(
        field: str, client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test create topic with missing field."""
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


class TestUpdateTopic:
    """Test topic update API."""

    @staticmethod
    def test_update_with_bad_credentials(client: Client, topic_fixture: Topic) -> None:
        """Test update api with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_update", args=[topic_fixture.pk])
        response = client.put(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_update_api(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test update topic."""
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
    def test_update_api_with_no_permission(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test update topic with no permission."""
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
    def test_update_api_missing_field(
        field: str, client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test update topic with missing field."""
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


class TestPatchTopic:
    """Test topic patch API."""

    @staticmethod
    def test_patch_with_bad_credentials(client: Client, topic_fixture: Topic) -> None:
        """Test patch api with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_patch", args=[topic_fixture.pk])
        response = client.patch(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_patch_api(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test patch topic."""
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
    def test_patch_api_with_no_permission(
        client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test update topic with no permission."""
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
    def test_patch_api_missing_field(
        field: str, client: Client, user_fixture: User, topic_fixture: Topic
    ) -> None:
        """Test patch topic with missing field."""
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
    """Test topic delete API."""

    @staticmethod
    def test_delete_with_bad_credentials(client: Client, topic_fixture: Topic) -> None:
        """Test delete api with bad credentials."""
        url = reverse_lazy("api-1.0.0:topic_detail", args=[topic_fixture.pk])
        response = client.delete(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_delete_api(
        client: Client, topic_fixture: Topic, user_fixture: User
    ) -> None:
        """Test topic delete API."""
        permission = Permission.objects.get(name="Can delete topic")
        user_fixture.user_permissions.add(permission)
        user_fixture.save()
        url = reverse_lazy("api-1.0.0:topic_delete", args=[topic_fixture.pk])
        response = client.delete(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        assert response.status_code == HTTPStatus.OK
        assert len(Topic.objects.all()) == 0

    @staticmethod
    def test_delete_api_with_no_permission(
        client: Client, topic_fixture: Topic, user_fixture: User
    ) -> None:
        """Test topic delete API."""
        url = reverse_lazy("api-1.0.0:topic_delete", args=[topic_fixture.pk])
        response = client.delete(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"message": NO_PERMISSION}
