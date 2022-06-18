import os
from datetime import timedelta

from celery import Celery


# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postbank-api.settings')

app = Celery('postbank')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sync_traders': {
        'task': 'sync_traders',
        'schedule': timedelta(hours=1)
    },
    'sync_bank_employees': {
        'task': 'sync_bank_employees',
        'schedule': timedelta(hours=1)
    },
    'sync_terminals': {
        'task': 'sync_terminals',
        'schedule': timedelta(hours=1)
    },
    'send_offers_notif': {
        'task': 'send_offers_notif',
        'schedule': crontab(hour=7, minute=30, day_of_week=3)
    }
}
