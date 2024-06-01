from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Events

@shared_task
def send_event_notifications():
    now = timezone.now()
    start_window = now + timedelta(minutes=30)
    events = Events.objects.filter(start_time__range=[now, start_window])
    for event in events:
        # Replace this with your actual notification logic
        print(f"Send notification for event: {event.name}")
