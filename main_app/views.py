from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """Home view for the main app.

    Args:
        request (HttpRequest): _Hettp request from client.

    Returns:
        HttpResponse: Http response from server.
    """
    return HttpResponse(f"Hello {request.user}")
