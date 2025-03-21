from typing import Self

from django.db import models

from authentication.models import User


class Topic(models.Model):
    """Topic model."""

    name = models.CharField(max_length=50, blank=False, unique=True)
    parent_topic = models.ForeignKey(
        "Topic", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self: Self) -> str:
        """String representation of the model."""
        return f"{self.name}"


class Post(models.Model):
    """Post model."""

    title = models.CharField(max_length=200, blank=False)
    topic = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to="posts")
    content = models.CharField(blank=False)
    previous = models.ForeignKey(
        "Post", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self: Self) -> str:
        """String representation of the model."""
        return f"{self.title}"

    @property
    def next(self: Self) -> "Post":
        """Get post that references this instance as previoues.

        Returns:
            Post: Post object.
        """
        return Post.objects.filter(previous=self).first()
