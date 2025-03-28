"""
Scheduled tasks for the events app.
"""
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.db.models import F

from events.models import Event, Registration
from telegram_bot.bot import send_telegram_notification

@shared_task
def update_event_statuses():
    """
    Task to automatically update event statuses.
    Events that have passed their date will be marked as completed.
    """
    now = timezone.now()
    
    # Update events where date is in the past and status is still active
    events_updated = Event.objects.filter(
        date__lt=now,
        status=Event.Status.ACTIVE
    ).update(status=Event.Status.COMPLETED)
    
    return f"Updated {events_updated} events to completed status"

@shared_task
def send_event_reminders():
    """
    Task to send reminders to participants about upcoming events.
    Sends reminders 24 hours before event start.
    """
    now = timezone.now()
    reminder_time = now + timedelta(hours=24)
    
    # Get events starting in approximately 24 hours
    upcoming_events = Event.objects.filter(
        date__range=(now, reminder_time),
        status=Event.Status.ACTIVE
    )
    
    reminders_sent = 0
    for event in upcoming_events:
        # Get all registrations for this event
        registrations = Registration.objects.filter(event=event)
        
        # Process reminders for each registration
        for registration in registrations:
            user = registration.user
            if user.telegram_username:
                # Here you would typically send a message via Telegram
                # For now we'll just print it
                message = f"Reminder: The event '{event.title}' you registered for is happening tomorrow at {event.date.strftime('%H:%M')}!"
                print(f"Sending reminder to {user.username} ({user.telegram_username}): {message}")
                # In a real app, you would call a function to send the Telegram message
                # send_telegram_message(user.telegram_username, message)
                reminders_sent += 1
    
    return f"Sent {reminders_sent} event reminders"

@shared_task
def send_new_events_digest():
    """
    Task to send a digest of new events to users.
    Collects events created in the last 24 hours.
    """
    yesterday = timezone.now() - timedelta(days=1)
    
    # Get events created in the last 24 hours
    new_events = Event.objects.filter(
        created_at__gte=yesterday,
        status=Event.Status.ACTIVE
    )
    
    if new_events.exists():
        # Create a digest message
        message = "New volunteer opportunities available:\n\n"
        for event in new_events:
            message += f"• {event.title} ({event.category.name}) - {event.date.strftime('%Y-%m-%d %H:%M')}\n"
            message += f"  Location: {event.location}\n"
            message += f"  Available spots: {event.capacity - event.registrations.count()}\n\n"
        
        # Send as a notification via Telegram
        try:
            send_telegram_notification({
                'title': 'New Events Digest',
                'message': message
            })
            return f"Sent digest with {new_events.count()} new events"
        except Exception as e:
            return f"Failed to send digest: {str(e)}"
    
    return "No new events to digest"