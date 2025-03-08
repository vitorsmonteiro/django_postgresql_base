from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime
from ninja import Field, Router, Schema

from todo.forms import TaskForm
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

    title: str = ""
    description: str = ""
    status: str = "new"


@router.get("/task", response=list[TaskOut])
def list_taks(request: HttpRequest) -> HttpResponse:
    """List tasks of the user."""
    query_set = Task.objects.filter(created_by=request.user)
    return query_set.order_by("id")


@router.post("/task")
def create_task(request: HttpRequest, payload: TaskIn) -> HttpResponse:
    """Create task API."""
    form = TaskForm(data=payload.dict())
    if form.is_valid():
        task: Task = form.save(commit=False)
        task.created_by = request.user
        task.save()
        return {"id": task.pk}
    return JsonResponse(data={"error": form.errors}, status=HTTPStatus.BAD_REQUEST)


@router.get("/task/{task_id}", response=TaskOut)
def detail_task(request: HttpRequest, task_id: int) -> HttpResponse:  # noqa: ARG001
    """Get task detail API.

    Args:
        request (HttpRequest): HttpRequest object
        task_id (int): Task Id

    Returns:
        HttpResponse: HttpResponse object containing task detail..
    """
    return get_object_or_404(Task, pk=task_id)


@router.put("/task/{task_id}", response=TaskOut)
def update_task(request: HttpRequest,  task_id: int, payload: TaskIn) -> HttpResponse:  # noqa: ARG001
    """Update task API.

    Args:
        request (HttpRequest): HttpRequest object
        task_id (int): Task Id
        payload (TaskIn): TaskIn object

    Returns:
        HttpResponse: HttpResponse object
    """
    task = get_object_or_404(Task, id=task_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(task, attr, value)
    task.save()
    return task


@router.delete("/task/{task_id}")
def delete_task(request: HttpRequest, task_id: int) -> HttpResponse:  # noqa: ARG001
    """Delete task API.

    Args:
        request (HttpRequest): HttpRequest object
        task_id (int): Task Id

    Returns:
        HttpResponse: HttpResponse object
    """
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return {"success": True}
