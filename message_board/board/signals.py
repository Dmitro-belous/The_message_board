from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Response, Announcement

from .tasks import send_approval, send_created_response, send_rejection, send_created_announcement


@receiver(post_save, sender=Response)
def my_handler(instance, created, **kwargs):
    if instance.status:

        send_approval.delay(instance.response_user.username, instance.response_post.head, instance.response_post.id,
                            instance.response_user.email)

    if created:

        send_created_response.delay(instance.response_post.author.username, instance.response_post.head, instance.id,
                                    instance.response_post.id, instance.response_post.author.email)


@receiver(post_delete, sender=Response)
def my_another_handler(instance, **kwargs):

    send_rejection.delay(instance.response_user.username, instance.response_post.head, instance.response_post.id,
                         instance.response_user.email)


@receiver(post_save, sender=Announcement)
def my_another_handler(instance, **kwargs):

    send_created_announcement.delay(instance.author.username, instance.head, instance.id, instance.author.email)
