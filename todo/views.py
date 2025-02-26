from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from todo.forms import TaskForm
from todo.models import Task, TaskCategory, TaskStatus


def home(request: HttpRequest) -> HttpResponse:
    """Todo home view.

    Args:
        request (HttpRequest): HttpRequest object

    Returns:
        HttpResponse: HttpResponse object
    """
    tasks = Task.objects.all()
    context = {"tasks": tasks}

    return render(request=request, template_name="todo/todo.html", context=context)


def create_todo(request: HttpRequest) -> HttpResponse:
    """Create todo view.

    Args:
        request (HttpRequest): HttpRequest object

    Returns:
        HttpResponse: HttpResponse object
    """
    if request.method == "GET":
        statuses = TaskStatus.objects.all()
        categories = TaskCategory.objects.all()
        context = {"statuses": statuses, "categories": categories}
        return render(
            request=request, template_name="todo/todo_create.html", context=context
        )
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("Task created successfully!")
    context = {"form": form}
    return render(
        request=request, template_name="todo/todo_create.html", context=context
    )
