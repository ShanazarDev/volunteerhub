"""
Services for events app - contains business logic that is not directly tied to views
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.conf import settings


def send_registration_confirmation_email(user, event):
    """
    Send an email to a user when they register for an event.
    """
    subject = _('Registration Confirmation: {0}').format(event.title)
    
    # Prepare email context
    context = {
        'user': user,
        'event': event,
        'site_name': 'VolunteerHub',
    }
    
    # Render email templates
    html_message = render_to_string('events/emails/registration_confirmation.html', context)
    plain_message = render_to_string('events/emails/registration_confirmation.txt', context)
    
    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False
    )


def send_registration_cancellation_email(user, event):
    """
    Send an email to a user when they cancel their registration for an event.
    """
    subject = _('Registration Cancellation: {0}').format(event.title)
    
    # Prepare email context
    context = {
        'user': user,
        'event': event,
        'site_name': 'VolunteerHub',
    }
    
    # Render email templates
    html_message = render_to_string('events/emails/registration_cancellation.html', context)
    plain_message = render_to_string('events/emails/registration_cancellation.txt', context)
    
    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False
    )