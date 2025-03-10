from typing import ClassVar, Self

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.forms import TopicForm
from blog.models import Topic
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
    success_url = reverse_lazy("todo:home")
    context_object_name = "topic"
    permission_required: ClassVar[list[str]] = ["blog.change_topic"]


class TopicDelete(PermissionRequiredMixin, DeleteView):
    """Topic generic delete view."""

    model = TopicForm
    template_name = "todo/topic_confirm_delete.html"
    success_url = reverse_lazy("blog:topic_delete")
    context_object_name = "topic"
    permission_required: ClassVar[list[str]] = ["blog.delete_topic"]
