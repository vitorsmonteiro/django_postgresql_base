from typing import Self

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from main_project.settings import PAGINATION_SIZE
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
    paginator = Paginator(tasks, PAGINATION_SIZE)
    page_obj = paginator.get_page(1)
    context = {"page_obj": page_obj}
    return render(request=request, template_name="todo/task_list.html", context=context)


class TaskList(LoginRequiredMixin, ListView):
    """Task generic list view."""

    model = Task
    template_name = "todo/components/task_table.html"
    context_object_name = "tasks"
    paginate_by = PAGINATION_SIZE
    ordering = "created_at"

    def get_queryset(self: Self) -> QuerySet:
        """Get filtered query set.

        Returns:
            QuerySet: Task queryset.
        """
        query_set = super().get_queryset()
        query_set = query_set.filter(created_by=self.request.user)
        if sort := self.request.GET.get("sort", ""):
            query_set = query_set.order_by(sort)
        if status := self.request.GET.get("status", ""):
            query_set = query_set.filter(status=status)
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


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Task generic update view."""

    model = Task
    template_name = "todo/task_update.html"
    form_class = TaskForm
    success_url = reverse_lazy("todo:home")
    context_object_name = "task"

    def test_func(self: Self) -> bool:
        """Test if user can update a task."""
        task: Task = self.get_object()
        return self.request.user == task.created_by


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Task generic delete view."""

    model = Task
    template_name = "todo/task_confirm_delete.html"
    success_url = reverse_lazy("todo:home")
    context_object_name = "task"

    def test_func(self: Self) -> bool:
        """Test if user can update a task."""
        task: Task = self.get_object()
        return self.request.user == task.created_by


class TaskDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Task generic detail view."""

    model = Task
    template_name = "todo/task_detail.html"
    context_object_name = "task"

    def test_func(self: Self) -> bool:
        """Test if user can update a task."""
        task: Task = self.get_object()
        return self.request.user == task.created_by
