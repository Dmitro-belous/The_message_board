from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Announcement


@shared_task
def my_job():

    mailing_list = list(
        User.objects.all(
        ).values_list(
            'username',
            'first_name',
            'email',
        )
    )

    posts_list = list(
        Announcement.objects.filter(
            time_add__gt=timezone.now() - timedelta(days=1)
        ))

    if len(mailing_list) > 0 and len(posts_list) > 0:
        for user, first_name, email in mailing_list:
            if not first_name:
                first_name = user

            html_content = render_to_string(
                'daily_posts.html',
                {
                    'name': first_name,
                    'posts': posts_list,
                    'link': settings.SITE_URL
                }
            )

            message = EmailMultiAlternatives(
                subject=f'Announcements for the day',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]

            )
            message.attach_alternative(html_content, 'text/html')
            message.send()


@shared_task
def send_approval(user, post, pk, email):

    text = f'Hello, {user}! Your response to the announcement "{post}" has been accepted!\n' \
           f'Announcement link: {settings.SITE_URL}/announcements/{pk}'
    html_content = render_to_string(
        'response_approved_email.html',
        {
            'user': user,
            'link': f'{settings.SITE_URL}/announcements/{pk}',
            'announcement': post
        }
    )

    msg = EmailMultiAlternatives(
        subject='Your response has been accepted',
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email, ],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_created_response(author, post, response_pk, post_pk, email):

    text = f'Hello, {author}! A new response has been left on your announcement "{post}"!\n'\
           f'Response link: {settings.SITE_URL}/announcements/response/{response_pk}\n' \
           f'Announcement link: {settings.SITE_URL}/announcements/{post_pk}'
    html_content = render_to_string(
        'response_created_email.html',
        {
            'user': author,
            'announcement_link': f'{settings.SITE_URL}/announcements/{post_pk}',
            'response_link': f'{settings.SITE_URL}/announcements/response/{response_pk}',
            'announcement': post
        }
    )

    msg = EmailMultiAlternatives(
        subject='A new response',
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email, ],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_rejection(user, post, pk, email):

    text = f'Hello, {user}! Your response to the announcement "{post}" has been rejected...\n' \
           f'Announcement link: {settings.SITE_URL}/announcements/{pk}'
    html_content = render_to_string(
        'response_rejected_email.html',
        {
            'user': user,
            'link': f'{settings.SITE_URL}/announcements/{pk}',
            'announcement': post
        }
    )

    msg = EmailMultiAlternatives(
        subject='Your response has been rejected',
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email, ],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_created_announcement(author, post, pk, email):

    text = f'Hello, {author}! Your announcement "{post}" has been successfully created!\n' \
           f'Announcement link: {settings.SITE_URL}/announcements/{pk}'
    html_content = render_to_string(
        'post_created_email.html',
        {
            'user': author,
            'link': f'{settings.SITE_URL}/announcements/{pk}',
            'announcement': post
        }
    )

    msg = EmailMultiAlternatives(
        subject='Your announcement has been created',
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email, ],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
