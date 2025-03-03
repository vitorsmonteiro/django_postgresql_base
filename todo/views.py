from typing import Self

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from todo.forms import TaskForm
from todo.models import Task


class TaskList(LoginRequiredMixin, ListView):
    """Task generic list view."""

    model = Task
    template_name = "todo/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self: Self) -> QuerySet:
        """Get filtered query set.

        Returns:
            QuerySet: Task queryset.
        """
        query_set = Task.objects.filter(created_by=self.request.user)
        query_set = query_set.order_by("created_at")
        return super().get_queryset()


class TaskCreate(LoginRequiredMixin, CreateView):
    """Task generic create view."""

    model = Task
    template_name = "todo/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("todo:home")


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """Task generic update view."""

    model = Task
    template_name = "todo/task_update.html"
    form_class = TaskForm
    success_url = reverse_lazy("todo:home")
    context_object_name = "task"


class TaskDelete(LoginRequiredMixin, DeleteView):
    """Task generic delete view."""

    model = Task
    template_name = "todo/task_confirm_delete.html"
    success_url = reverse_lazy("todo:home")
    context_object_name = "task"
