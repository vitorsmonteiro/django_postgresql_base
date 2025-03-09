import json
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse_lazy

from authentication.models import User
from todo.models import Task

pytestmark = pytest.mark.django_db


class TestListAPI:
    """Test list api."""

    @staticmethod
    def test_list_api_bad_credentials(client: Client) -> None:
        """Test viewlist api with bad credentials."""
        url = reverse_lazy("api-1.0.0:task_list")
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_list_api(client: Client, user_fixture: User, task_fixture: Task) -> None:
        """Test list api."""
        url = reverse_lazy("api-1.0.0:task_list")
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        expected = {
            "items": [
                {
                    "id": task_fixture.pk,
                    "title": task_fixture.title,
                    "description": task_fixture.description,
                    "status": task_fixture.status,
                    "created_by": task_fixture.created_by.email,
                    "created_at": task_fixture.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )[:-4]
                    + "Z",
                    "updated_at": task_fixture.updated_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )[:-4]
                    + "Z",
                },
            ],
            "count": len(Task.objects.filter(created_by=user_fixture)),
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected

    @staticmethod
    def test_list_api_qith_status_query(client: Client, user_fixture: User) -> None:
        """Test list api with different user."""
        url = reverse_lazy("api-1.0.0:task_list")
        response = client.get(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            query_params={"status": "foo"},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "items": [],
            "count": len(Task.objects.filter(created_by=user_fixture, status="foo")),
        }

    @staticmethod
    def test_list_api_different_user(client: Client, user_fixture2: User) -> None:
        """Test list api with different user."""
        url = reverse_lazy("api-1.0.0:task_list")
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture2.token}"}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "items": [],
            "count": len(Task.objects.filter(created_by=user_fixture2)),
        }


class TestCreateAPI:
    """Test create api."""

    @staticmethod
    def test_create_api_bad_credentials(client: Client) -> None:
        """Test create api with bad credentials."""
        url = reverse_lazy("api-1.0.0:task_create")
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_create_api(client: Client, user_fixture: User) -> None:
        """Test create api."""
        data = {"title": "title", "description": "description", "status": "new"}
        url = reverse_lazy("api-1.0.0:task_create")
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        task = Task.objects.first()
        excpected = {
            "id": task.pk,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_by": task.created_by.email,
            "created_at": task.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z",
            "updated_at": task.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z",
        }
        assert len(Task.objects.all()) == 1
        assert response.status_code == HTTPStatus.OK
        assert response.json() == excpected

    @staticmethod
    def test_create_api_errors(client: Client, user_fixture: User) -> None:
        """Test create api."""
        data = {"title": "title", "description": "description", "status": "New"}
        url = reverse_lazy("api-1.0.0:task_create")
        response = client.post(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        assert len(Task.objects.all()) == 0
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
        assert response.json() == {
            "detail": [
                {
                    "type": "value_error",
                    "loc": ["body", "payload", "status"],
                    "msg": (
                        f"Value error, '{data['status']}' is not a valid status. "
                        f"Valid options: {", ".join(Task.STATUS_CHOICES.keys())}"
                    ),
                    "ctx": {
                        "error": (
                            f"'{data['status']}' is not a valid status. "
                            f"Valid options: {", ".join(Task.STATUS_CHOICES.keys())}"
                        )
                    },
                }
            ]
        }


class TestDetailAPI:
    """Test detail api."""

    @staticmethod
    def test_detail_api_bad_credentials(client: Client, task_fixture: Task) -> None:
        """Test viewdetail api with bad credentials."""
        url = reverse_lazy("api-1.0.0:task_detail", args=[task_fixture.pk])
        response = client.get(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_detail_api(client: Client, user_fixture: User, task_fixture: Task) -> None:
        """Test detail api."""
        url = reverse_lazy("api-1.0.0:task_detail", args=[task_fixture.pk])
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        expected = {
            "id": task_fixture.pk,
            "title": task_fixture.title,
            "description": task_fixture.description,
            "status": task_fixture.status,
            "created_by": task_fixture.created_by.email,
            "created_at": task_fixture.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]
            + "Z",
            "updated_at": task_fixture.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]
            + "Z",
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected

    @staticmethod
    def test_detail_api_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test detail api with different user."""
        url = reverse_lazy("api-1.0.0:task_detail", args=[task_fixture.pk])
        response = client.get(
            url, headers={"Authorization": f"Bearer {user_fixture2.token}"}
        )
        assert response.status_code == HTTPStatus.FORBIDDEN


class TestPatchAPI:
    """Test patch api."""

    @staticmethod
    def test_patch_api_bad_credentials(client: Client, task_fixture: Task) -> None:
        """Test patch api with bad credentials."""
        url = reverse_lazy("api-1.0.0:task_patch", args=[task_fixture.pk])
        response = client.patch(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_patch_api(client: Client, user_fixture: User, task_fixture: Task) -> None:
        """Test patch api."""
        data = {"title": "test"}
        url = reverse_lazy("api-1.0.0:task_patch", args=[task_fixture.pk])
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        task_fixture.refresh_from_db()
        expected = {
            "id": task_fixture.pk,
            "title": "test",
            "description": task_fixture.description,
            "status": task_fixture.status,
            "created_by": task_fixture.created_by.email,
            "created_at": task_fixture.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]
            + "Z",
            "updated_at": task_fixture.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]
            + "Z",
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected

    @staticmethod
    def test_patch_api_with_invalid_status(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test patch api with invalid status."""
        data = {"status": "foo"}
        url = reverse_lazy("api-1.0.0:task_patch", args=[task_fixture.pk])
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        task_fixture.refresh_from_db()
        assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
        assert response.json() == {
            "detail": [
                {
                    "type": "value_error",
                    "loc": ["body", "payload", "status"],
                    "msg": (
                        f"Value error, '{data['status']}' is not a valid status. "
                        f"Valid options: {", ".join(Task.STATUS_CHOICES.keys())}"
                    ),
                    "ctx": {
                        "error": (
                            f"'{data['status']}' is not a valid status. "
                            f"Valid options: {", ".join(Task.STATUS_CHOICES.keys())}"
                        )
                    },
                }
            ]
        }

    @staticmethod
    def test_patch_api_with_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test patch api with different user."""
        data = {"title": "test"}
        url = reverse_lazy("api-1.0.0:task_patch", args=[task_fixture.pk])
        response = client.patch(
            url,
            headers={"Authorization": f"Bearer {user_fixture2.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        task_fixture.refresh_from_db()
        assert response.status_code == HTTPStatus.FORBIDDEN


class TestUpdateAPI:
    """Test update api."""

    @staticmethod
    def test_update_api_bad_credentials(client: Client, task_fixture: Task) -> None:
        """Test update api with bad credentials."""
        url = reverse_lazy("api-1.0.0:task_update", args=[task_fixture.pk])
        response = client.put(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_update_api(client: Client, user_fixture: User, task_fixture: Task) -> None:
        """Test update api."""
        data = {"title": "title", "description": "description", "status": "new"}
        url = reverse_lazy("api-1.0.0:task_update", args=[task_fixture.pk])
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        task_fixture.refresh_from_db()
        expected = {
            "id": task_fixture.pk,
            "title": data["title"],
            "description": data["description"],
            "status": data["status"],
            "created_by": task_fixture.created_by.email,
            "created_at": task_fixture.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]
            + "Z",
            "updated_at": task_fixture.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]
            + "Z",
        }
        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected

    @staticmethod
    def test_update_api_with_invalid_status(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test update api with invalid status."""
        data = {"title": "title", "description": "description", "status": "staus"}
        url = reverse_lazy("api-1.0.0:task_update", args=[task_fixture.pk])
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
                    "type": "value_error",
                    "loc": ["body", "payload", "status"],
                    "msg": (
                        f"Value error, '{data['status']}' is not a valid status. "
                        f"Valid options: {", ".join(Task.STATUS_CHOICES.keys())}"
                    ),
                    "ctx": {
                        "error": (
                            f"'{data['status']}' is not a valid status. "
                            f"Valid options: {", ".join(Task.STATUS_CHOICES.keys())}"
                        )
                    },
                }
            ]
        }

    @staticmethod
    def test_update_api_with_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test update api with different user."""
        data = {"title": "title", "description": "description", "status": "new"}
        url = reverse_lazy("api-1.0.0:task_update", args=[task_fixture.pk])
        response = client.put(
            url,
            headers={"Authorization": f"Bearer {user_fixture2.token}"},
            data=json.dumps(data),
            content_type="application/json",
        )
        task_fixture.refresh_from_db()
        assert response.status_code == HTTPStatus.FORBIDDEN


class TestDeleteAPI:
    """Test delete api."""

    @staticmethod
    def test_delete_api_bad_credentials(client: Client, task_fixture: Task) -> None:
        """Test delete api with bad credentials."""
        url = reverse_lazy("api-1.0.0:task_delete", args=[task_fixture.pk])
        response = client.delete(url, headers={"Authorization": "Bearer test"})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @staticmethod
    def test_delete_api(client: Client, user_fixture: User, task_fixture: Task) -> None:
        """Test delete api."""
        assert len(Task.objects.all()) == 1
        url = reverse_lazy("api-1.0.0:task_delete", args=[task_fixture.pk])
        response = client.delete(
            url, headers={"Authorization": f"Bearer {user_fixture.token}"}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "success"}
        assert len(Task.objects.all()) == 0

    @staticmethod
    def test_delete_api_with_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test delete api with different user."""
        url = reverse_lazy("api-1.0.0:task_delete", args=[task_fixture.pk])
        response = client.delete(
            url,
            headers={"Authorization": f"Bearer {user_fixture2.token}"},
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
