from datetime import datetime

from django.http import HttpRequest, HttpResponse
from ninja import Field, Router, Schema
from ninja.pagination import paginate

from blog.models import BlogPost, Topic

router = Router()


class TopicOut(Schema):
    """Topic API out schema."""

    id: int
    name: str


class PostOut(Schema):
    """Post API Output schema."""

    id: int
    title: str
    topic: str = Field(..., alias="topic.name")
    author: str = Field(..., alias="name.email")
    content: str
    created_at: datetime
    updated_at: datetime
    previous: int


@router.get("/topic", response=list[TopicOut], url_name="topic_list")
@paginate()
def list_topic(request: HttpRequest, sort: str = "id") -> HttpResponse:  # noqa:ARG001
    """Topic list API.

    Args:
        request (HttpRequest): HttpRequest object.
        sort (str, optional): Sort list by sort value. Defaults to "id".

    Returns:
        HttpResponse: HttpResponse object.
    """
    query_set = Topic.objects.all()
    return query_set.order_by(sort)


@router.get("/topic", response=list[TopicOut], url_name="post_list")
@paginate()
def list_post(
    request: HttpRequest,  # noqa:ARG001
    sort: str = "id",
    topic: str | None = None,
) -> HttpResponse:
    """Post list API.

    Args:
        request (HttpRequest): HttpRequest object.
        sort (str, optional): Sort list by sort value. Defaults to "id".
        topic (str | None, optional): Filter posts based on topic name.
          Defaults to None-

    Returns:
        HttpResponse: HttpResponse object.
    """
    query_set = BlogPost.objects.all()
    if topic:
        query_set = query_set.filter(topic__name=topic)
    return query_set.order_by(sort)
