from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from todo.models import Task


def todo(request: HttpRequest) -> HttpResponse:
    """Todo home view.

    Args:
        request (HttpRequest): HttpRequest object

    Returns:
        HttpResponse: HttpResponse object
    """
    tasks = Task.objects.all()
    context = {"tasks": tasks}

    return render(request=request, template_name="todo/todo.html", context=context)
