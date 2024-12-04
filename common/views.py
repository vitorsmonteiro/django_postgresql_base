from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

app_name = "common"


def home(request: HttpRequest) -> HttpResponse:
    """Home view.

    Args:
        request (HttpRequest): Request

    Returns:
        HttpResponse: Response
    """
    return render(request, "common/home.html")
