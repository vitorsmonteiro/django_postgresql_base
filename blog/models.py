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


class BlogPost(models.Model):
    """Post model."""

    title = models.CharField(max_length=200, blank=False)
    topic = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to="posts")
    content = models.CharField(blank=False)
    previous = models.ForeignKey(
        "BlogPost", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self: Self) -> str:
        """String representation of the model."""
        return f"{self.title}"

    @property
    def next(self: Self) -> "BlogPost":
        """Get post that references this instance as previoues.

        Returns:
            Post: Post object.
        """
        return BlogPost.objects.filter(previous=self).first()


class Commment(models.Model):
    """Comment model."""

    blog_post: BlogPost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author: User = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self: Self) -> str:
        """String representation of the model."""
        return f"{self.author.email} - {self.blog_post.title}"
