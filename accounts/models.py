from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adding additional fields for user roles and profile information.
    """
    class Role(models.TextChoices):
        VOLUNTEER = 'volunteer', _('Volunteer')
        ORGANIZER = 'organizer', _('Organizer')
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VOLUNTEER,
        help_text=_('Defines the user role and permissions')
    )
    
    bio = models.TextField(
        blank=True,
        help_text=_('A brief description about the user')
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('Contact phone number')
    )
    
    telegram_username = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Telegram username for notifications')
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def is_organizer(self):
        """Check if user has organizer role"""
        return self.role == self.Role.ORGANIZER
