from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from decouple import config

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE', default='config.settings.dev'))

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Define the Celery-Beat schedules
app.conf.beat_schedule = {
    # 'fetch-and-store-portfolio-values-every-night': {
    #     'task': 'stats.tasks.fetch_and_store_portfolio_values',
    #     'schedule': crontab(hour=0, minute=0),  # Every midnight
    # },
    # Add other celery-beat schedules here as needed
    'fetch-and-store-portfolio-values-every-night': {
        'task': 'stats.tasks.fetch_and_store_portfolio_values',
        'schedule': crontab(minute='*'),  # Every minute for testing
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
