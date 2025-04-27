from pathlib import Path

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from blog.models import BlogPost, Commment
from blog.tasks import send_email


@receiver(post_save, sender=Commment)
def notification_email(sender: BlogPost, instance: BlogPost, **kwargs: str) -> None:  # noqa:ARG001
    """Send email when comment is saved."""
    send_email.delay_on_commit(instance.pk)


@receiver(post_delete, sender=BlogPost)
def delete_image_file(sender: BlogPost, instance: BlogPost, **kwargs: str) -> None:  # noqa:ARG001
    """Delete image after instance is removed."""
    image = instance.image
    if image:
        path = Path(image.path)
        if path.exists():
            path.unlink()
