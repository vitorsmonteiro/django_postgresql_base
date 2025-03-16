from pathlib import Path

from django.db.models.signals import post_delete
from django.dispatch import receiver

from authentication.models import User


@receiver(post_delete, sender=User)
def delete_image_file(sender: User, instance: User, **kwargs: str) -> None:  # noqa:ARG001
    """Delete image after instance is removed."""
    image = instance.profile_image
    if image:
        path = Path(image.path)
        if path.exists():
            path.unlink()
