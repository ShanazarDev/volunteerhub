from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import OrganizerRating, VolunteerRating


@receiver(post_save, sender=OrganizerRating)
def update_organizer_rating_stats(sender, instance, **kwargs):
    """
    When an organizer is rated, update their average rating in profile or stats.
    This could be used for sorting/filtering organizers by rating later.
    """
    organizer = instance.organizer
    
    # Calculate new average rating
    avg_rating = OrganizerRating.objects.filter(
        organizer=organizer
    ).aggregate(avg=Avg('rating'))['avg'] or 0
    
    # You can store this in User model if needed, or in a separate stats model


@receiver(post_save, sender=VolunteerRating)
def update_volunteer_rating_stats(sender, instance, **kwargs):
    """
    When a volunteer is rated, update their average rating in profile or stats.
    This could be used for recognizing top volunteers later.
    """
    volunteer = instance.volunteer
    
    # Calculate new average rating
    avg_rating = VolunteerRating.objects.filter(
        volunteer=volunteer
    ).aggregate(avg=Avg('rating'))['avg'] or 0
    
    # You can store this in User model if needed, or in a separate stats model