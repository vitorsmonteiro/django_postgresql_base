from datetime import datetime
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Field, File, Form, Router, Schema, UploadedFile
from ninja.pagination import paginate

from blog.models import BlogPost, Topic

router = Router()
NO_PERMISSION = "User does not have permission."


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
    parent_topic: str | None = Field(None, alias="parent_topic.name")


class BlogPostIn(Schema):
    """BlogPost API input schema."""

    title: str
    topic: int | None = None
    content: str
    previous: int | None = ""


class BlogPostPathIn(Schema):
    """BlogPost API input schema."""

    title: str = ""
    topic: str | None = None
    content: str = ""
    previous: int | None = None


class BlogPostOut(Schema):
    """BlogPost API Output schema."""

    id: int
    title: str
    topic: str | None = Field(None, alias="topic.name")
    author: str | None = Field(None, alias="author.email")
    content: str
    created_at: datetime
    previous: str | None = Field(None, alias="previous.title")


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


@router.get("/topic/{topic_id}", response=TopicOut, url_name="topic_detail")
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
    response={
        HTTPStatus.OK: TopicOut,
        HTTPStatus.BAD_REQUEST: Message,
        HTTPStatus.UNAUTHORIZED: Message,
    },
)
def create_topic(request: HttpRequest, payload: TopicIn) -> HttpResponse:
    """Topic create API.

    Args:
        request (HttpRequest): HttpRequest object.
        payload (TopicIn): Topic creation schema.

    Returns:
        HttpResponse: HttpResponse object.
    """
    if not request.user.has_perm("blog.add_topic"):
        return HTTPStatus.UNAUTHORIZED, {"message": NO_PERMISSION}
    topic = Topic.objects.create(name=payload.name)
    if payload.parent_topic:
        parent_topic = get_object_or_404(Topic, pk=payload.parent_topic)
        topic.parent_topic = parent_topic
        topic.save()
    return HTTPStatus.OK, topic


@router.put(
    "/topic/{topic_id}",
    url_name="topic_update",
    response={
        HTTPStatus.OK: TopicOut,
        HTTPStatus.BAD_REQUEST: Message,
        HTTPStatus.UNAUTHORIZED: Message,
    },
)
def update_topic(request: HttpRequest, topic_id: int, payload: TopicIn) -> HttpResponse:
    """Topic update API.

    Args:
        request (HttpRequest): HttpRequest object.
        topic_id (int): Topic id.
        payload (TopicIn): Topic creation schema.

    Returns:
        HttpResponse: HttpResponse object.
    """
    if not request.user.has_perm("blog.change_topic"):
        return HTTPStatus.UNAUTHORIZED, {"message": NO_PERMISSION}
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.name = payload.name
    if payload.parent_topic:
        parent_topic = get_object_or_404(Topic, pk=payload.parent_topic)
        topic.parent_topic = parent_topic
    else:
        topic.parent_topic = None
    topic.save()
    return HTTPStatus.OK, topic


@router.patch(
    "/topic/{topic_id}",
    url_name="topic_patch",
    response={
        HTTPStatus.OK: TopicOut,
        HTTPStatus.BAD_REQUEST: Message,
        HTTPStatus.UNAUTHORIZED: Message,
    },
)
def patch_topic(
    request: HttpRequest,
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
    if not request.user.has_perm("blog.change_topic"):
        return HTTPStatus.UNAUTHORIZED, {"message": NO_PERMISSION}
    topic = get_object_or_404(Topic, pk=topic_id)
    if payload.name:
        topic.name = payload.name
    if payload.parent_topic:
        topic.parent_topic = payload.parent_topic
    topic.save()
    return HTTPStatus.OK, topic


@router.delete(
    "/topic/{topic_id}",
    url_name="topic_delete",
    response={HTTPStatus.OK: None, HTTPStatus.UNAUTHORIZED: Message},
)
def delete_topic(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Topic delete API.

    Args:
        request (HttpRequest): HttpRequest object.
        topic_id (int): Topic id.

    Returns:
        HttpResponse: HttpResponse object.
    """
    if not request.user.has_perm("blog.delete_topic"):
        return HTTPStatus.UNAUTHORIZED, {"message": NO_PERMISSION}
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.delete()
    return HTTPStatus.OK


@router.get("/blog_post", response=list[BlogPostOut], url_name="blog_post_list")
@paginate()
def list_blog_post(request: HttpRequest, sort: str = "id") -> HttpResponse:  # noqa:ARG001
    """Blog post list API.

    Args:
        request (HttpRequest): HttpRequest object.
        sort (str, optional): Sort list by sort value. Defaults to "id".

    Returns:
        HttpResponse: HttpResponse object.
    """
    query_set = BlogPost.objects.all()
    return query_set.order_by(sort)


@router.get("/blog_post/{post_id}", response=BlogPostOut, url_name="blog_post_detail")
def detail_blog_post(request: HttpRequest, post_id: int) -> HttpResponse:  # noqa:ARG001
    """Blog post detail API.

    Args:
        request (HttpRequest): HttpRequest object.
        post_id (int): BlogPost id.

    Returns:
        HttpResponse: HttpResponse object.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    return HTTPStatus.OK, post


@router.post(
    "/blog_post",
    url_name="blog_post_create",
    response={HTTPStatus.OK: BlogPostOut, HTTPStatus.BAD_REQUEST: Message},
)
def create_blog_post(
    request: HttpRequest,
    payload: Form[BlogPostIn],
    image: File[UploadedFile],
) -> HttpResponse:
    """BlogPost create API.

    Args:
        request (HttpRequest): HttpRequest object.
        payload (Form[BlogPostIn]): BlogPost creation schema.
        image (File[UploadedFile]): Blog post image

    Returns:
        HttpResponse: HttpResponse object.
    """
    topic = get_object_or_404(Topic, pk=payload.topic)
    post = BlogPost.objects.create(
        title=payload.title, topic=topic, author=request.user, content=payload.content
    )
    if payload.previous:
        previous = get_object_or_404(BlogPost, pk=payload.previous)
        post.previous = previous
    if image:
        extension = image.name.split(".")[-1]
        new_image_name = f"post_{post.pk}.{extension}"
        image.name = new_image_name
        post.image = image
    post.save()
    return HTTPStatus.OK, post


@router.put(
    "/blog_post/{post_id}",
    url_name="blog_post_update",
    response={HTTPStatus.OK: BlogPostOut, HTTPStatus.BAD_REQUEST: Message},
)
def update_blog_post(
    request: HttpRequest,  # noqa: ARG001
    post_id: int,
    payload: BlogPostIn,
) -> HttpResponse:
    """Topic update API.

    Args:
        request (HttpRequest): HttpRequest object.
        post_id (int): BlogPost id.
        payload (BlogPostIn): BlogPost creation schema.

    Returns:
        HttpResponse: HttpResponse object.
    """
    topic = get_object_or_404(Topic, pk=payload.topic)
    post = get_object_or_404(BlogPost, pk=post_id)
    post.title = payload.title
    post.topic = topic
    post.content = payload.content
    if payload.previous:
        previous = get_object_or_404(BlogPost, pk=payload.previous)
        post.previous = previous
    post.save()
    return HTTPStatus.OK, post


@router.patch(
    "/blog_post/{post_id}",
    url_name="blog_post_patch",
    response={HTTPStatus.OK: BlogPostOut, HTTPStatus.BAD_REQUEST: Message},
)
def patch_blog_post(
    request: HttpRequest,  # noqa: ARG001
    post_id: int,
    payload: BlogPostPathIn,
) -> HttpResponse:
    """Topic patch API.

    Args:
        request (HttpRequest): HttpRequest object.
        post_id (int): BlogPost id.
        payload (BlogPostPathIn): BlogPost creation schema.

    Returns:
        HttpResponse: HttpResponse object.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    if payload.title:
        post.title = payload.title
    if payload.topic:
        topic = get_object_or_404(Topic, pk=payload.topic)
        post.topic = topic
    if payload.content:
        post.content = payload.content
    if payload.previous:
        previous = get_object_or_404(BlogPost, pk=payload.previous)
        post.previous = previous
    post.save()
    return HTTPStatus.OK, post


@router.delete("/blog_post/{post_id}", url_name="blog_post_delete")
def delete_blog_post(request: HttpRequest, post_id: int) -> HttpResponse:  # noqa:ARG001
    """Topic delete API.

    Args:
        request (HttpRequest): HttpRequest object.
        post_id (int): BlogPost id.

    Returns:
        HttpResponse: HttpResponse object.
    """
    post = get_object_or_404(BlogPost, pk=post_id)
    post.delete()
    return HTTPStatus.OK
