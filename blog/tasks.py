from django.core.mail import EmailMultiAlternatives

from blog.models import Comment
from celery import shared_task


@shared_task
def send_email(commment_id: int) -> None:
    """Send email when comment is updated."""
    commment = Comment.objects.get(pk=commment_id)
    email = EmailMultiAlternatives(
        subject="Test",
        body=f"{commment.comment}",
        from_email="test@email.com",
        to=["vitors.monteiro1@gmail.com"],
    )
    email.send()
