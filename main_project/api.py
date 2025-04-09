from http import HTTPStatus
from typing import Self

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.security import HttpBearer

from authentication.models import User
from blog.api.api_v1 import router as blog_router_v1
from todo.api.api_v1 import router as todo_router_v1


class GlobalAuth(HttpBearer):
    """Global API authentication."""

    def authenticate(self: Self, request: HttpRequest, token: str) -> User:
        """Authenticate user based on token.

        Args:
            request (HttpRequest): HttpRequestObbject.
            token (str): User token.

        Raises:
            PermissionDenied: Raised if user with the given token is not found.

        Returns:
            User: User object
        """
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist as exc:
            raise PermissionDenied from exc
        else:
            request.user = user
            return user


api_v1 = NinjaAPI(version="1.0.0", auth=GlobalAuth(), title="VitorXYZ API Docs")

api_v1.add_router("/todo/", todo_router_v1)
api_v1.add_router("/blog/", blog_router_v1)


@api_v1.exception_handler(PermissionDenied)
def permission_denied(request: HttpRequest, _: Exception) -> HttpResponse:
    """Permission denied response.

    Args:
        request (HttpRequest): HttpRequest object.
        exc (Exception): Exception

    Returns:
        HttpResponse: Http response object
    """
    return api_v1.create_response(
        request=request,
        data={"error": "Bad credentials"},
        status=HTTPStatus.UNAUTHORIZED,
    )
