import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domain_monitor.settings')

# autodiscover tasks from installed apps
app = Celery('domain_monitor')
app.config_from_object('django.conf:settings', namespace='CELERY')
# This line tells Celery to automatically discover tasks from all installed Django apps.
# It is necessary to ensure that Celery can find and execute the tasks defined in the apps.
app.autodiscover_tasks()
# This means that Celery will look for settings that start with 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Define the Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'check-domain-status-every-5-minutes': {
        'task': 'monitoring.tasks.check_domain_status',
        'schedule': crontab(minute='*/5'),
    },
}