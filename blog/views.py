from typing import ClassVar, Self

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.forms import PostForm, TopicForm
from blog.models import Post, Topic
from main_project.settings import PAGINATION_SIZE


class TopicList(LoginRequiredMixin, ListView):
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


class TopicCreate(PermissionRequiredMixin, CreateView):
    """Topic generic create view."""

    model = Topic
    template_name = "blog/topic_create.html"
    form_class = TopicForm
    success_url = reverse_lazy("blog:topic_list")
    permission_required: ClassVar[list[str]] = ["blog.add_topic"]


class TopicUpdate(PermissionRequiredMixin, UpdateView):
    """Topic generic update view."""

    model = Topic
    template_name = "blog/topic_update.html"
    form_class = TopicForm
    success_url = reverse_lazy("blog:topic_list")
    context_object_name = "topic"
    permission_required: ClassVar[list[str]] = ["blog.change_topic"]


class TopicDelete(PermissionRequiredMixin, DeleteView):
    """Topic generic delete view."""

    model = TopicForm
    template_name = "blog/topic_confirm_delete.html"
    success_url = reverse_lazy("blog:topic_delete")
    context_object_name = "topic"
    permission_required: ClassVar[list[str]] = ["blog.delete_topic"]


class PostList(LoginRequiredMixin, ListView):
    """Post generic list view."""

    model = Post
    context_object_name = "posts"
    paginate_by = PAGINATION_SIZE

    def get_template_names(self: Self) -> str:
        """Get template name based on request type."""
        if self.request.headers.get("Hx-Request", False):
            return "blog/components/post_table.html"
        return "blog/post_list.html"

    def get_queryset(self: Self) -> QuerySet:
        """Get queryset data based on request type."""
        query_set = Post.objects.all()
        query_set = query_set.order_by("title")
        if self.request.headers.get("Hx-Request", False):
            search = self.request.GET.get("search", "")
            query_set = query_set.filter(title__startswith=search)
        return query_set


class PostCreate(PermissionRequiredMixin, CreateView):
    """Topic generic create view."""

    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:post_list")
    permission_required: ClassVar[list[str]] = ["blog.add_post"]

    def get_context_data(self: Self, **kwargs: str) -> dict:
        """Override to pass extra context."""
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        context["posts"] = Post.objects.all()
        return context

    def form_valid(self: Self, form: PostForm) -> HttpResponse:
        """Save image with standard_name."""
        if form.is_valid():
            title = form.cleaned_data["title"]
            topic = form.cleaned_data["topic"]
            author = self.request.user
            content = form.cleaned_data["content"]
            post = Post(title=title, topic=topic, author=author, content=content)
            post.save()
            image: UploadedFile = form.cleaned_data["image"]
            if image:
                extension = image.name.split(".")[-1]
                image.name = (f"post_{post.pk}.{extension}")
                post.image = image
                post.save()
        return HttpResponseRedirect(reverse_lazy("blog:post_list"))


class PostUpdate(PermissionRequiredMixin, UpdateView):
    """Post generic update view."""

    model = Post
    template_name = "blog/post_update.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:post_list")
    context_object_name = "post"
    permission_required: ClassVar[list[str]] = ["blog.change_post"]

    def get_context_data(self: Self, **kwargs: str) -> dict:
        """Override to pass extra context."""
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        context["posts"] = Post.objects.all()
        return context

    def form_valid(self: Self, form: PostForm) -> HttpResponse:
        """Save image with standard_name."""
        if form.is_valid():
            title = form.cleaned_data["title"]
            topic = form.cleaned_data["topic"]
            author = self.request.user
            content = form.cleaned_data["content"]
            post = Post(title=title, topic=topic, author=author, content=content)
            post.save()
            image: UploadedFile = form.cleaned_data["image"]
            if image and form.changed_data.get("image"):
                extension = image.name.split(".")[-1]
                image.name = (f"post_{post.pk}.{extension}")
                post.image = image
                post.save()
        return HttpResponseRedirect(reverse_lazy("blog:post_list"))

class PostDetail(DetailView):
    """Post generic detail view."""

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostDelete(PermissionRequiredMixin, DeleteView):
    """Post generic delete view."""

    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    context_object_name = "post"
    permission_required: ClassVar[list[str]] = ["blog.delete_topic"]
