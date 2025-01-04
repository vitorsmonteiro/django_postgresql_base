from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def todo(request: HttpRequest) -> HttpResponse:
    """Todo view.

    Args:
        request (HttpRequest): HttpRequest object

    Returns:
        HttpResponse: HttpResponse object
    """
    return render(request=request, template_name="todo/todo.html")
