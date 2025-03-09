from http import HTTPStatus

import pytest
from django.test import Client, RequestFactory
from django.urls import reverse_lazy

from authentication.models import User
from conftest import USER_PASSWORD
from todo import views
from todo.models import Task

pytestmark = pytest.mark.django_db
factory = RequestFactory()


class TestHomeView:
    """Test home view."""

    @staticmethod
    def test_home_view_no_login(client: Client) -> None:
        """Test home view with user not loged."""
        url = reverse_lazy("todo:home")
        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_home_view(user_fixture: User, task_fixture: Task) -> None:
        """Tesh home view with user that has tasks."""
        url = reverse_lazy("todo:home")
        request = factory.get(url)
        request.user = user_fixture
        response = views.home(request=request)
        assert response.status_code == HTTPStatus.OK
        assert task_fixture.title in str(response.content)

    @staticmethod
    def test_home_view_no_tasks(user_fixture2: User, task_fixture: Task) -> None:
        """Tesh home view with user that has no tasks."""
        url = reverse_lazy("todo:home")
        request = factory.get(url)
        request.user = user_fixture2
        response = views.home(request=request)
        assert response.status_code == HTTPStatus.OK
        assert task_fixture.title not in str(response.content)


class TestTaskListView:
    """Test TaskList view."""

    @staticmethod
    def test_list_view_no_login(client: Client) -> None:
        """Test list view with user not loged."""
        url = reverse_lazy("todo:task_list")
        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_list_own_tasks(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test list view with user that has tasks."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_list")
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert task_fixture.title in str(response.content)

    @staticmethod
    def test_list_filter_status(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test list view with status filter."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_list")
        response = client.get(url, query_params={"status": "done"})
        assert response.status_code == HTTPStatus.OK
        assert task_fixture.title not in str(response.content)

    @staticmethod
    def test_list_sort(client: Client, user_fixture: User, task_fixture: Task) -> None:
        """Test list view with sort query."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_list")
        response = client.get(url, query_params={"sort": "created_by"})
        assert response.status_code == HTTPStatus.OK
        assert task_fixture.title in str(response.content)

    @staticmethod
    def test_list_no_tasks(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test list view with user that has no tasks."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture2.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_list")
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert task_fixture.title not in str(response.content)


class TestCreateView:
    """Test create view."""

    @staticmethod
    def test_create_get_view_no_login(client: Client) -> None:
        """Test create view with user not loged."""
        url = reverse_lazy("todo:task_create")
        response = client.get(url)
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_create_post_view_no_login(client: Client) -> None:
        """Test create post view with user not loged."""
        url = reverse_lazy("todo:task_create")
        response = client.post(url)
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_create_get_view(client: Client, user_fixture: User) -> None:
        """Test create get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_create")
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_create_post_view(client: Client, user_fixture: User) -> None:
        """Test create post view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_create")
        data = {"title": "title", "description": "description", "status": "new"}
        response = client.post(url, data=data)
        task = Task.objects.first()
        assert response.status_code == HTTPStatus.FOUND
        assert task.title == data["title"]
        assert task.description == data["description"]
        assert task.status == data["status"]

    @staticmethod
    def test_create_post_view_error(client: Client, user_fixture: User) -> None:
        """Test create post view with validation error."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_create")
        data = {"title": "title", "description": "description", "status": "nNew"}
        response = client.post(url, data=data)
        task = Task.objects.first()
        assert response.status_code == HTTPStatus.OK
        assert task is None


class TestUpdateView:
    """Test update view."""

    @staticmethod
    def test_update_get_view_no_login(client: Client, task_fixture: Task) -> None:
        """Test update view with user not loged."""
        url = reverse_lazy("todo:task_update", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_update_post_view_no_login(client: Client, task_fixture: Task) -> None:
        """Test update post view with user not loged."""
        url = reverse_lazy("todo:task_update", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_update_get_view(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test update get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_update", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_update_get_view_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test update get view with different user."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture2.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_update", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FORBIDDEN

    @staticmethod
    def test_update_post_view(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test update post view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_update", args=[task_fixture.pk])
        data = {"title": "title", "description": "description", "status": "new"}
        response = client.post(url, data=data, args=[task_fixture.pk])
        task_fixture.refresh_from_db()
        assert response.status_code == HTTPStatus.FOUND
        assert task_fixture.title == data["title"]
        assert task_fixture.description == data["description"]
        assert task_fixture.status == data["status"]

    @staticmethod
    def test_update_post_view_validation_error(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test update post view with validation view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_update", args=[task_fixture.pk])
        data = {"title": "title", "description": "description", "status": "New"}
        response = client.post(url, data=data, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_update_post_view_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test update post view with different user."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture2.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_update", args=[task_fixture.pk])
        data = {"title": "title", "description": "description", "status": "New"}
        response = client.post(url, data=data, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FORBIDDEN


class TestDetailView:
    """Test detail view."""

    @staticmethod
    def test_detail_get_view_no_login(client: Client, task_fixture: Task) -> None:
        """Test detail view with user not loged."""
        url = reverse_lazy("todo:task_detail", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_detail_post_view_no_login(client: Client, task_fixture: Task) -> None:
        """Test detail post view with user not loged."""
        url = reverse_lazy("todo:task_detail", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_detail_get_view(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test detail get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_detail", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.OK


class TestDeleteView:
    """Test delete view."""

    @staticmethod
    def test_delete_get_view_no_login(client: Client, task_fixture: Task) -> None:
        """Test delete view with user not loged."""
        url = reverse_lazy("todo:task_delete", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_delete_post_view_no_login(client: Client, task_fixture: Task) -> None:
        """Test delete post view with user not loged."""
        url = reverse_lazy("todo:task_delete", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FOUND

    @staticmethod
    def test_delete_get_view(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test delete get view."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_delete", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_delete_get_view_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test delete get view with different user."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture2.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_delete", args=[task_fixture.pk])
        response = client.get(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FORBIDDEN

    @staticmethod
    def test_delete_post_view(
        client: Client, user_fixture: User, task_fixture: Task
    ) -> None:
        """Test delete post view."""
        assert len(Task.objects.all()) == 1
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_delete", args=[task_fixture.pk])
        response = client.delete(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FOUND
        assert len(Task.objects.all()) == 0

    @staticmethod
    def test_delete_post_view_different_user(
        client: Client, user_fixture2: User, task_fixture: Task
    ) -> None:
        """Test delete post view with different user."""
        login_url = reverse_lazy("authentication:login")
        client.post(
            login_url, data={"email": user_fixture2.email, "password": USER_PASSWORD}
        )
        url = reverse_lazy("todo:task_delete", args=[task_fixture.pk])
        response = client.post(url, args=[task_fixture.pk])
        assert response.status_code == HTTPStatus.FORBIDDEN
