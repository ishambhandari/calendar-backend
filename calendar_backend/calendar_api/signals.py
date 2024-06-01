from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Events
from .tasks import send_event_notifications

@receiver(post_save, sender=Events)
def schedule_email_reminder(sender, instance, created, **kwargs):
    if created:
        start_time = instance.start_time
        reminder_time = start_time - timezone.timedelta(minutes=10)
        send_email_reminder.apply_async((instance.id,), eta=reminder_time)


