from http import HTTPStatus
from typing import Any, ClassVar, Self

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import BlogPostForm, CommentForm, TopicForm
from blog.models import BlogPost, Comment, Topic
from main_project.settings import PAGINATION_SIZE


class TopicListView(ListView):
    """List topic generic view."""

    model = Topic
    context_object_name = "topics"
    paginate_by = PAGINATION_SIZE

    def get_template_names(self: Self) -> str:
        """Get template name based on request type."""
        if self.request.headers.get("Hx-Request", False):
            return "blog/components/topic_table.html"
        return "blog/topic_list.html"

    def get_queryset(self: Self) -> QuerySet:
        """Get queryset data based on request type."""
        query_set = Topic.objects.all()
        query_set = query_set.order_by("name")
        if self.request.headers.get("Hx-Request", False):
            search = self.request.GET.get("search", "")
            query_set = query_set.filter(name__startswith=search)
        return query_set


class TopicCreateView(PermissionRequiredMixin, CreateView):
    """Topic generic create view."""

    model = Topic
    template_name = "blog/topic_create.html"
    form_class = TopicForm
    success_url = reverse_lazy("blog:topic_list")
    permission_required: ClassVar[list[str]] = ["blog.add_topic"]

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add context data."""
        context = super().get_context_data(**kwargs)
        context["topic_choices"] = Topic.objects.all()
        return context


class TopicDetailView(DetailView):
    """Topic generic detail view."""

    model = Topic
    template_name = "blog/topic_detail.html"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add context data."""
        context = super().get_context_data(**kwargs)
        context["posts"] = BlogPost.objects.filter(topic=self.get_object())
        return context


class TopicUpdateView(PermissionRequiredMixin, UpdateView):
    """Topic generic update view."""

    model = Topic
    template_name = "blog/topic_update.html"
    form_class = TopicForm
    success_url = reverse_lazy("blog:topic_list")
    context_object_name = "topic"
    permission_required: ClassVar[list[str]] = ["blog.change_topic"]

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add context data."""
        context = super().get_context_data(**kwargs)
        context["topic_choices"] = Topic.objects.all()
        return context


class TopicDeleteView(PermissionRequiredMixin, DeleteView):
    """Topic generic delete view."""

    model = Topic
    template_name = "blog/topic_confirm_delete.html"
    success_url = reverse_lazy("blog:topic_list")
    context_object_name = "topic"
    permission_required: ClassVar[list[str]] = ["blog.delete_topic"]


class BlogPostListView(ListView):
    """Post generic list view."""

    model = BlogPost
    context_object_name = "posts"
    paginate_by = PAGINATION_SIZE

    def get_template_names(self: Self) -> str:
        """Get template name based on request type."""
        if self.request.headers.get("Hx-Request", False):
            return "blog/components/post_table.html"
        return "blog/post_list.html"

    def get_queryset(self: Self) -> QuerySet:
        """Get queryset data based on request type."""
        query_set = BlogPost.objects.all()
        query_set = query_set.order_by("title")
        if self.request.headers.get("Hx-Request", False):
            if search := self.request.GET.get("search"):
                query_set = query_set.filter(title__startswith=search)
            if topic := self.request.GET.get("topic"):
                query_set = query_set.filter(topic=topic)
        return query_set

    def get_context_data(self: Self, **kwargs: str) -> dict:
        """Override to pass extra context."""
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        return context


class BlogPostCreateView(PermissionRequiredMixin, CreateView):
    """Topic generic create view."""

    model = BlogPost
    template_name = "blog/post_create.html"
    form_class = BlogPostForm
    success_url = reverse_lazy("blog:post_list")
    permission_required: ClassVar[list[str]] = ["blog.add_blogpost"]

    def get_context_data(self: Self, **kwargs: str) -> dict:
        """Override to pass extra context."""
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        context["posts"] = BlogPost.objects.all()
        return context

    def form_valid(self: Self, form: BlogPostForm) -> HttpResponse:
        """Save image with standard_name."""
        if form.is_valid():
            title = form.cleaned_data["title"]
            topic = form.cleaned_data["topic"]
            author = self.request.user
            content = form.cleaned_data["content"]
            previous = form.cleaned_data.get("previous")
            post = BlogPost.objects.create(
                title=title,
                topic=topic,
                author=author,
                content=content,
                previous=previous,
            )
            image: UploadedFile = form.cleaned_data.get("image")
            if image:
                extension = image.name.split(".")[-1]
                new_image_name = f"post_{post.pk}.{extension}"
                image.name = new_image_name
                post.image = image
            post.save()
            return HttpResponseRedirect(reverse_lazy("blog:post_list"))
        return render(self.request, "blog/post_create.html", context={"form": form})


class BlogPostUpdateView(PermissionRequiredMixin, UpdateView):
    """Post generic update view."""

    model = BlogPost
    template_name = "blog/post_update.html"
    form_class = BlogPostForm
    success_url = reverse_lazy("blog:post_list")
    context_object_name = "post"
    permission_required: ClassVar[list[str]] = ["blog.change_blogpost"]

    def get_context_data(self: Self, **kwargs: str) -> dict:
        """Override to pass extra context."""
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        context["posts"] = BlogPost.objects.all()
        return context

    def form_valid(self: Self, form: BlogPostForm) -> HttpResponse:
        """Save image with standard_name."""
        if form.is_valid():
            post: BlogPost = form.instance
            title = form.cleaned_data["title"]
            topic = form.cleaned_data["topic"]
            content = form.cleaned_data["content"]
            previous = form.cleaned_data.get("previous")
            post.title = title
            post.topic = topic
            post.content = content
            if previous:
                post.previous = previous
            image: UploadedFile = form.cleaned_data.get("image")
            if image and "image" in form.changed_data:
                extension = image.name.split(".")[-1]
                new_image_name = f"post_{post.pk}.{extension}"
                image.name = new_image_name
                post.image = image
            post.save()
            return HttpResponseRedirect(reverse_lazy("blog:post_list"))
        return render(self.request, "blog/post_update.html", context={"form": form})


class BlogPostDetailView(DetailView):
    """Post generic detail view."""

    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class BlogPostDeleteView(PermissionRequiredMixin, DeleteView):
    """Post generic delete view."""

    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    context_object_name = "post"
    permission_required: ClassVar[list[str]] = ["blog.delete_blogpost"]


def add_post_comment(request: HttpRequest) -> HttpResponse:
    """Add post comment."""
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            blog_post: BlogPost = form.cleaned_data["blog_post"]
            content = form.cleaned_data["content"]
            Comment.objects.create(author=author, blog_post=blog_post, content=content)
            blog_post.refresh_from_db()
            return render(
                request,
                "blog/components/comment_list.html",
                context={"post": blog_post},
            )
    return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)


def remove_post_comment(request: HttpRequest, pk: int) -> HttpResponse:
    """Remove post comment.

    Args:
        request (HttpRequest): HttpRequest object
        pk (int): Post ID

    Returns:
        HttpResponse: HttpResponse object
    """
    comment = Comment.objects.get(pk=pk)
    blog_post = comment.blog_post
    comment.delete()
    blog_post.refresh_from_db()
    return render(
        request,
        "blog/components/comment_list.html",
        context={"post": blog_post},
    )
