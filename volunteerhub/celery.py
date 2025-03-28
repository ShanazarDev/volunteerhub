import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'volunteerhub.settings')

app = Celery('volunteerhub')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-event-statuses': {
        'task': 'events.tasks.scheduled.update_event_statuses',
        'schedule': crontab(minute='0', hour='*/1'),  # Run every hour
    },
    'send-event-reminders': {
        'task': 'events.tasks.scheduled.send_event_reminders',
        'schedule': crontab(minute='0', hour='9'),  # Run daily at 9 AM
    },
    'send-new-events-digest': {
        'task': 'events.tasks.scheduled.send_new_events_digest',
        'schedule': crontab(minute='0', hour='18'),  # Run daily at 6 PM
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')