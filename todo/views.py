from typing import Self

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from todo.forms import TaskForm
from todo.models import Task


@login_required
def home(request: HttpRequest) -> HttpResponse:
    """Todo home view.

    Args:
        request (HttpRequest): Http request object.

    Returns:
        HttpResponse: Http response object
    """
    tasks = Task.objects.filter(created_by=request.user)
    tasks = tasks.order_by("created_at")
    context = {"tasks": tasks}
    return render(request=request, template_name="todo/task_list.html", context=context)


class TaskList(LoginRequiredMixin, ListView):
    """Task generic list view."""

    model = Task
    template_name = "todo/components/task_table.html"
    context_object_name = "tasks"

    def get_queryset(self: Self) -> QuerySet:
        """Get filtered query set.

        Returns:
            QuerySet: Task queryset.
        """
        query_set = Task.objects.filter(created_by=self.request.user)
        if sort := self.request.GET.get("sort"):
            query_set = query_set.order_by(sort)
        for item in self.request.GET.items():
            if item[1] and item[0] != "sort":
                query_set = query_set.filter(item)
        return query_set


class TaskCreate(LoginRequiredMixin, CreateView):
    """Task generic create view."""

    model = Task
    template_name = "todo/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("todo:home")

    def form_valid(self: Self, form: TaskForm) -> HttpResponse:
        """Override the form valid metod to add created_by.

        Args:
            form (TaskForm): Task form object

        Returns:
            HttpResponse: Http response object
        """
        task: Task = form.save(commit=False)
        task.created_by = self.request.user
        task.save()
        return super().form_valid(form)


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
