from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import EventFeedback, OrganizerRating, VolunteerRating


@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    """
    Admin configuration for EventFeedback model.
    """
    list_display = ('user', 'event', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'event__status')
    search_fields = ('user__username', 'user__email', 'event__title', 'comment')
    raw_id_fields = ('user', 'event')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(OrganizerRating)
class OrganizerRatingAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrganizerRating model.
    """
    list_display = ('volunteer', 'organizer', 'event', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = (
        'volunteer__username', 'volunteer__email',
        'organizer__username', 'organizer__email',
        'event__title', 'comment'
    )
    raw_id_fields = ('volunteer', 'organizer', 'event')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(VolunteerRating)
class VolunteerRatingAdmin(admin.ModelAdmin):
    """
    Admin configuration for VolunteerRating model.
    """
    list_display = ('organizer', 'volunteer', 'event', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = (
        'organizer__username', 'organizer__email',
        'volunteer__username', 'volunteer__email',
        'event__title', 'comment'
    )
    raw_id_fields = ('organizer', 'volunteer', 'event')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)