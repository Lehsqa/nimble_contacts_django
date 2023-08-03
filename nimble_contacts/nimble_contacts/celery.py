import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nimble_contacts.settings')

app = Celery('nimble_contacts')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_contacts_daily': {
        'task': 'contacts.tasks.update_contacts',
        'schedule': crontab(hour=0, minute=0),
        'args': (16, 16)
    }
}

app.autodiscover_tasks()
