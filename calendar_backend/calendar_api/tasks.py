from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Events

@shared_task
def send_event_notification(event_id, receiver_email):
    print("event instance", event_id)
    event_instance = Events.objects.get(id = event_id)
    print('event_instance', event_instance.title)
    try:
        subject = "Event Reminder"
        message = f"Reminder: Your event {event_instance.title} starts in 15 minutes"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [receiver_email],  # Sending to the creator of the event
        )
        print("Email sent successfully!")  # Add a print statement for successful email sending
        print(f"even.created_by.{receiver_email} email", receiver_email)
    except Exception as e:
        print(f"An error occurred while sending email: {e}")  # Print the error message if an exception occurs
