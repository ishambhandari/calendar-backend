from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
# from datetime import timedelta

from django.utils import timezone

@shared_task
def send_event_notifications(events_id):
    from .models import Events
    from_email = settings.EMAIL_HOST_USER
    try:
        events = Events.objects.get(id=events_id)
        # events = Events.objects.filter(start_time__range=[now, start_window])
        subject = "Events Reminder"
        message = f"Reminder: Your work {work.title} starts soon"
        send_mail(
                subject,
                message,
                from_email,
                [events.user.email],
                )
    except:
        print("Error!")


