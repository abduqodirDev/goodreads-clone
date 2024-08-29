from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser
from users.tasks import send_email


@receiver(post_save, sender=CustomUser)
def send_email_to_celery(sender, instance, created, *args, **kwargs):
    if created:
        if instance.email:
            send_email(
                "Welcome to Goodreads clone",
                f"Hi, {instance.username}. Welcome to goodreads clome, enjoy books and reviews.",
                [instance.email]
            )
