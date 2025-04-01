from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from telegram_bot.bot import send_telegram_notification


@receiver(post_save, sender=Event)
def event_saved(sender, instance, created, **kwargs):
    """
    Signal to send Telegram notification when a new event is created.
    """
    if created and instance.status == Event.Status.ACTIVE:
        send_telegram_notification(instance)
