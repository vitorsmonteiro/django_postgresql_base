from typing import ClassVar, Self

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords

from main_app.managers import CachedManager

CAR_CACHE_KEY = "car_data"
MANUFACTURER_CACHE_KEY = "manufacturer_data"


class Manufacturer(models.Model):
    """Manufacturer model."""

    name = models.CharField(max_length=100, unique=True)

    objects = CachedManager(cache_key=MANUFACTURER_CACHE_KEY)
    history = HistoricalRecords()

    def __str__(self: Self) -> str:
        """Retunt the string representation of the model."""
        return f"{self.name}"


class Car(models.Model):
    """Car model."""

    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    objects = CachedManager(cache_key=CAR_CACHE_KEY)
    history = HistoricalRecords()

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


@receiver([post_save, post_delete], sender=Car, weak=True)
@receiver([post_save, post_delete], sender=Manufacturer, weak=True)
def update_manufacturer_cache(sender: models.Model, **kwargs) -> None:  # noqa: ANN003, ARG001:
    """Update cached date."""
    cache.delete(MANUFACTURER_CACHE_KEY)
    cache.delete(CAR_CACHE_KEY)
    car_data = Car.objects.all()
    man_data = Manufacturer.objects.all()
    cache.set(CAR_CACHE_KEY, car_data)
    cache.set(MANUFACTURER_CACHE_KEY, man_data)
