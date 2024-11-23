from typing import Self

from django.core.cache import cache
from django.db import models


class CachedManager(models.Manager):
    """Cache manager."""

    def __init__(self: Self, cache_key: str) -> None:
        """Initialize the cache manaher by receing the cache key.

        Args:
            cache_key (str): Cache key to store/fetch data
        """
        self.cache_key = cache_key
        super().__init__()

    def get_queryset(self: Self) -> models.QuerySet:
        """Get queryset method for django models."""
        if self.cache_key is None:
            error_text = "Please previde a valid cahcke key."
            raise (KeyError(error_text))

        data = cache.get(self.cache_key)

        if not data:
            # Fetch data from the database
            data = super().get_queryset()
            # Cache the data
            cache.set(self.cache_key, data, timeout=None)

        return data
