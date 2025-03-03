from typing import ClassVar, Self

from django.db import models

from authentication.models import User


class Task(models.Model):
    """Task model."""

    STATUS_CHOICES: ClassVar[dict] = {
        "new": "New",
        "in progress": "In progress",
        "done": "Done",
    }

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS_CHOICES)

    def __str__(self: Self) -> str:
        """String representation."""
        return f"Task ID: {self.pk}"
