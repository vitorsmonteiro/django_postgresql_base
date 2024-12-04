from typing import Self

from django.db import models

from authentication.models import User


class TaskCategory(models.Model):
    """Task category model."""

    name = models.CharField(max_length=50, blank=False)

    def __str__(self: Self) -> str:
        """String representation."""
        return f"Category: {self.name}"


class TaskStatus(models.Model):
    """Task status model."""

    name = models.CharField(max_length=50, blank=False)

    def __str__(self: Self) -> str:
        """String representation."""
        return f"Status: {self.name}"


class Task(models.Model):
    """Task model."""

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self: Self) -> str:
        """String representation."""
        return f"Task ID: {self.pk}"
