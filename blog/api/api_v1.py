from datetime import datetime
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Field, Router, Schema
from ninja.pagination import paginate

from blog.models import Topic

router = Router()


class TopicIn(Schema):
    """Topic API input schema."""

    name: str
    parent_topic: int | None


class TopicInPatch(Schema):
    """Topic API input patch schema."""

    name: str = ""
    parent_topic: int | None = None


class TopicOut(Schema):
    """Topic API output schema."""

    id: int
    name: str
    parent_topic: str = Field(..., alias="topic.name")


class PostIn(Schema):
    """Post API input schema."""

    title: str
    topic: str = Field(..., alias="topic.name")
    author: str = Field(..., alias="name.email")
    content: str
    created_at: datetime
    updated_at: datetime
    image: str
    previous: int


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


class Message(Schema):
    """Generic schema for messages."""

    message: str


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


@router.get("/topic", response=TopicOut, url_name="topic_detail")
def detail_topic(request: HttpRequest, topic_id: int) -> HttpResponse:  # noqa:ARG001
    """Topic detail API.

    Args:
        request (HttpRequest): HttpRequest object.
        topic_id (int): Topic id.

    Returns:
        HttpResponse: HttpResponse object.
    """
    topic = get_object_or_404(Topic, pk=topic_id)
    return HTTPStatus.OK, topic


@router.post(
    "/topic",
    url_name="topic_create",
    response={HTTPStatus.OK: TopicOut, HTTPStatus.BAD_REQUEST: Message},
)
def create_topic(request: HttpRequest, payload: TopicIn) -> HttpResponse:  # noqa:ARG001
    """Topic create API.

    Args:
        request (HttpRequest): HttpRequest object.
        payload (TopicIn): Topic creation schema.

    Returns:
        HttpResponse: HttpResponse object.
    """
    topic = Topic.objects.create(name=payload.name)
    if payload.parent_topic:
        topic.parent_topic = payload.parent_topic
        topic.save()
    return HTTPStatus.OK, topic


@router.put(
    "/topic",
    url_name="topic_update",
    response={HTTPStatus.OK: TopicOut, HTTPStatus.BAD_REQUEST: Message},
)
def update_topic(request: HttpRequest, topic_id: int, payload: TopicIn) -> HttpResponse:  # noqa:ARG001
    """Topic update API.

    Args:
        request (HttpRequest): HttpRequest object.
        topic_id (int): Topic id.
        payload (TopicIn): Topic creation schema.

    Returns:
        HttpResponse: HttpResponse object.
    """
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.name = payload.name
    if payload.parent_topic:
        topic.parent_topic = payload.parent_topic
    topic.save()
    return HTTPStatus.OK, topic


@router.patch(
    "/topic",
    url_name="topic_patch",
    response={HTTPStatus.OK: TopicOut, HTTPStatus.BAD_REQUEST: Message},
)
def patch_topic(
    request: HttpRequest,  # noqa:ARG001
    topic_id: int,
    payload: TopicInPatch,
) -> HttpResponse:
    """Topic patch API.

    Args:
        request (HttpRequest): HttpRequest object.
        topic_id (int): Topic id.
        payload (TopicInPatch): Topic creation schema.

    Returns:
        HttpResponse: HttpResponse object.
    """
    topic = get_object_or_404(Topic, pk=topic_id)
    if payload.name:
        topic.name = payload.name
    if payload.parent_topic:
        topic.parent_topic = payload.parent_topic
    topic.save()
    return HTTPStatus.OK, topic
