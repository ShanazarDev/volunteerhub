from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from events.models import Event


class EventFeedback(models.Model):
    """
    Model for users to provide feedback for events they attended.
    Users can rate the event and leave comments.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_feedback_given',
        verbose_name=_('User')
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='feedback',
        verbose_name=_('Event')
    )
    rating = models.PositiveSmallIntegerField(
        _('Rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rating from 1 to 5 stars')
    )
    comment = models.TextField(
        _('Comment'),
        blank=True,
        help_text=_('Optional feedback comment')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('event feedback')
        verbose_name_plural = _('event feedback')
        unique_together = ['user', 'event']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s feedback for {self.event.title} ({self.rating}★)"


class OrganizerRating(models.Model):
    """
    Model for volunteers to rate event organizers.
    This helps evaluate organizer performance and reputation.
    """
    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organizer_ratings_given',
        verbose_name=_('Volunteer')
    )
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organizer_ratings_received',
        verbose_name=_('Organizer')
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='organizer_ratings',
        verbose_name=_('Event')
    )
    rating = models.PositiveSmallIntegerField(
        _('Rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rating from 1 to 5 stars')
    )
    comment = models.TextField(
        _('Comment'),
        blank=True,
        help_text=_('Optional comment on organizer performance')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('organizer rating')
        verbose_name_plural = _('organizer ratings')
        unique_together = ['volunteer', 'organizer', 'event']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.volunteer.username}'s rating for organizer {self.organizer.username} ({self.rating}★)"


class VolunteerRating(models.Model):
    """
    Model for organizers to rate volunteers who participated in their events.
    This helps build volunteer reputation and acknowledge their contributions.
    """
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='volunteer_ratings_given',
        verbose_name=_('Organizer')
    )
    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='volunteer_ratings_received',
        verbose_name=_('Volunteer')
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='volunteer_ratings',
        verbose_name=_('Event')
    )
    rating = models.PositiveSmallIntegerField(
        _('Rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Rating from 1 to 5 stars')
    )
    comment = models.TextField(
        _('Comment'),
        blank=True,
        help_text=_('Optional comment on volunteer performance')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('volunteer rating')
        verbose_name_plural = _('volunteer ratings')
        unique_together = ['organizer', 'volunteer', 'event']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.organizer.username}'s rating for volunteer {self.volunteer.username} ({self.rating}★)"