from typing import Self

from django.db import models


class Topic(models.Model):
    """Topic model."""

    name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self: Self) -> str:
        """String representation of the model."""
        return f"{self.name}"
