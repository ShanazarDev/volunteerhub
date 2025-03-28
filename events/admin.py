from django.contrib import admin
from .models import Category, Event, Registration


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin configuration for Event model.
    """
    list_display = ('title', 'category', 'date', 'location', 'status', 'organizer', 'registered_count')
    list_filter = ('status', 'category', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    raw_id_fields = ('organizer',)
    
    def registered_count(self, obj):
        return obj.registrations.count()
    registered_count.short_description = 'Registered participants'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Registration model.
    """
    list_display = ('user', 'event', 'registered_at', 'attended')
    list_filter = ('attended', 'registered_at')
    search_fields = ('user__username', 'user__email', 'event__title')
    raw_id_fields = ('user', 'event')
