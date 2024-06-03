from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Events

@shared_task
def send_event_notification(event_id):
    try:
        event = Events.objects.get(id=event_id)
        subject = "Event Reminder"
        message = f"Reminder: Your event '{event.title}' starts soon"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [event.created_by.email],  # Sending to the creator of the event
        )
    except Events.DoesNotExist:
        print("Event not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
