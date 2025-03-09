from datetime import datetime
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Field, Router, Schema
from pydantic import field_validator

from todo.models import Task

router = Router()


class TaskOut(Schema):
    """Task API Output schema."""

    id: int
    title: str
    description: str
    status: str
    created_by: str = Field(..., alias="created_by.email")
    created_at: datetime
    updated_at: datetime


class TaskIn(Schema):
    """Task API Input schema."""

    title: str
    description: str
    status: str

    @field_validator("status")
    @staticmethod
    def validate_status(status: str) -> str:
        """Validate status against possible options.

        Args:
            status (str): Status value

        Raises:
            ValueError: Raised if status is not valid

        Returns:
            str: Status value
        """
        choices = Task.STATUS_CHOICES.keys()
        if status not in choices:
            msg = (
                f"'{status}' is not a valid status. Valid options: {", ".join(choices)}"
            )
            raise ValueError(msg)
        return status


class TaskInPatch(TaskIn):
    """Task Patch API Input schema."""

    title: str = ""
    description: str = ""
    status: str = ""


class Message(Schema):
    """Generic schema for messages."""

    message: str


@router.get("/task", response=list[TaskOut], url_name="task_list")
def list_taks(request: HttpRequest) -> HttpResponse:
    """List tasks of the user."""
    query_set = Task.objects.filter(created_by=request.user)
    return query_set.order_by("id")


@router.post(
    "/task",
    url_name="task_create",
    response={HTTPStatus.OK: TaskOut, HTTPStatus.BAD_REQUEST: Message},
)
def create_task(request: HttpRequest, payload: TaskIn) -> HttpResponse:
    """Create task API."""
    task = Task.objects.create(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        created_by=request.user,
    )
    return HTTPStatus.OK, task


@router.get(
    "/task/{task_id}",
    response={HTTPStatus.OK: TaskOut, HTTPStatus.FORBIDDEN: Message},
    url_name="task_detail",
)
def detail_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """Get task detail API.

    Args:
        request (HttpRequest): HttpRequest object
        task_id (int): Task Id

    Returns:
        HttpResponse: HttpResponse object containing task detail..
    """
    task = get_object_or_404(Task, pk=task_id)
    if task.created_by != request.user:
        return HTTPStatus.FORBIDDEN, {
            "message": "User does not have acces to resource."
        }
    return HTTPStatus.OK, task


@router.put(
    "/task/{task_id}",
    response={
        HTTPStatus.OK: TaskOut,
        HTTPStatus.BAD_REQUEST: Message,
        HTTPStatus.FORBIDDEN: Message,
    },
    url_name="task_update",
)
def update_task(request: HttpRequest, task_id: int, payload: TaskIn) -> HttpResponse:
    """Update task API.

    Args:
        request (HttpRequest): HttpRequest object
        task_id (int): Task Id
        payload (TaskIn): TaskIn object

    Returns:
        HttpResponse: HttpResponse object
    """
    task = get_object_or_404(Task, id=task_id)
    if task.created_by != request.user:
        return HTTPStatus.FORBIDDEN, {
            "message": "User does not have acces to resource."
        }
    task.title = payload.title
    task.description = payload.description
    task.status = payload.status
    task.save()
    task.refresh_from_db()
    return HTTPStatus.OK, task


@router.patch(
    "/task/{task_id}",
    response={HTTPStatus.OK: TaskOut, HTTPStatus.FORBIDDEN: Message},
    url_name="task_patch",
)
def patch_task(
    request: HttpRequest, task_id: int, payload: TaskInPatch
) -> HttpResponse:
    """Ptach task API.

    Args:
        request (HttpRequest): HttpRequest object
        task_id (int): Task Id
        payload (TaskIn): TaskIn object

    Returns:
        HttpResponse: HttpResponse object
    """
    task = get_object_or_404(Task, id=task_id)
    if task.created_by != request.user:
        return HTTPStatus.FORBIDDEN, {
            "message": "User does not have acces to resource."
        }
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(task, attr, value)
    task.save()
    return HTTPStatus.OK, task


@router.delete(
    "/task/{task_id}",
    url_name="task_delete",
    response={HTTPStatus.OK: Message, HTTPStatus.FORBIDDEN: Message},
)
def delete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """Delete task API.

    Args:
        request (HttpRequest): HttpRequest object
        task_id (int): Task Id

    Returns:
        HttpResponse: HttpResponse object
    """
    task = get_object_or_404(Task, id=task_id)
    if task.created_by != request.user:
        return HTTPStatus.FORBIDDEN, {
            "message": "User does not have acces to resource."
        }
    task.delete()
    return HTTPStatus.OK, {"message": "success"}
