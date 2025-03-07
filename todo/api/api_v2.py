from django.http import HttpRequest, HttpResponse
from ninja import Router, Schema

router = Router()


class HelloSchema(Schema):
    """Hello API Schema."""

    name: str


@router.post("/hello")
def hello(request: HttpRequest, data: HelloSchema) -> HttpResponse:
    """Test hello API.

    Args:
        request (HttpRequest): _description_
        data (_type_): _description_

    Returns:
        HttpResponse: _description_
    """
    return f"HELLLOOOOOO {data.name}"
