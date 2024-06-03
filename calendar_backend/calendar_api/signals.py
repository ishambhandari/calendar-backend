from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Events
from .tasks import send_event_notification

@receiver(post_save, sender=Events)
def schedule_email_reminder(sender, instance, created, **kwargs):
    if created:
        reminder_time = instance.start_time - timezone.timedelta(minutes=10)
        send_event_notification.apply_async((instance.id,), eta=reminder_time)
