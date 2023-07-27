import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_board.settings')

app = Celery('message_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_day_8am': {
        'task': 'board.tasks.my_job',
        'schedule': crontab(hour=8, minute=0),
    },
}
