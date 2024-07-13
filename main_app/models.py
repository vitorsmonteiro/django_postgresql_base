from typing import ClassVar, Self

from django.db import models


class Manufacturer(models.Model):
    """Manufacturer model."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self: Self) -> str:
        """Retunt the string representation of the model."""
        return f"{self.name}"


class Car(models.Model):
    """Car model."""

    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        """Model meta data."""

        unique_together: ClassVar[list[str]] = ["name", "manufacturer"]

    def __str__(self: Self) -> str:
        """Retunt the string representation of the model."""
        return f"{self.manufacturer}: {self.name}"

    def save(self: Self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Save model with full validations."""
        self.full_clean()
        return super().save(*args, **kwargs)
