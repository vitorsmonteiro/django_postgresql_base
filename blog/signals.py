from pathlib import Path

from django.db.models.signals import post_delete
from django.dispatch import receiver

from blog.models import Post


@receiver(post_delete, sender=Post)
def delete_image_file(sender: Post, instance: Post, **kwargs: str) -> None:  # noqa:ARG001
    """Delete image after instance is removed."""
    image = instance.image
    if image:
        path = Path(image.path)
        if path.exists():
            path.unlink()
