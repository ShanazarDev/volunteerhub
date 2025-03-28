from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Category(models.Model):
    """
    Event categories like animals, ecology, children, etc.
    """
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Volunteer events with details about date, location, capacity, etc.
    """
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')
    
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name=_('Category')
    )
    date = models.DateTimeField(_('Date and time'))
    location = models.CharField(_('Location'), max_length=255)
    capacity = models.PositiveIntegerField(_('Capacity (number of volunteers)'))
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events_created',
        verbose_name=_('Organizer')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    participants = models.ManyToManyField(
        User,
        through='Registration',
        related_name='events_registered',
        verbose_name=_('Participants')
    )
    
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('events:event_detail', args=[self.pk])
    
    @property
    def is_past(self):
        """Check if event date is in the past"""
        return self.date < timezone.now()
    
    @property
    def registered_count(self):
        """Get the number of registered participants"""
        return self.registrations.count()
    
    @property
    def available_spots(self):
        """Get the number of available spots"""
        return max(0, self.capacity - self.registered_count)


class Registration(models.Model):
    """
    Registration of users for events (many-to-many relationship)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name=_('User')
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name=_('Event')
    )
    registered_at = models.DateTimeField(_('Registered at'), auto_now_add=True)
    attended = models.BooleanField(_('Attended'), default=False)
    
    class Meta:
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')
        # Ensure a user can register only once for a specific event
        unique_together = ['user', 'event']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
