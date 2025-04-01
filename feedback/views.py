from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Count
from django.http import Http404

from events.models import Event, Registration
from accounts.models import User
from .models import EventFeedback, OrganizerRating, VolunteerRating
from .forms import EventFeedbackForm, OrganizerRatingForm, VolunteerRatingForm


@login_required
def event_feedback(request, event_id):
    """
    View for users to provide feedback for an event they attended.
    """
    event = get_object_or_404(Event, pk=event_id)
    
    registration = get_object_or_404(Registration, user=request.user, event=event)
    
    if not event.is_past:
        messages.error(request, _('You can only provide feedback for past events.'))
        return redirect('events:event_detail', pk=event_id)
    
    existing_feedback = EventFeedback.objects.filter(user=request.user, event=event).first()
    update = False
    
    if existing_feedback:
        update = True
        form = EventFeedbackForm(request.POST or None, instance=existing_feedback)
    else:
        form = EventFeedbackForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)
        if not update:
            feedback.user = request.user
            feedback.event = event
        feedback.save()
        
        messages.success(
            request, 
            _('Thank you! Your feedback has been submitted.') if not update else _('Your feedback has been updated.')
        )
        return redirect('events:event_detail', pk=event_id)
    
    context = {
        'form': form,
        'event': event,
        'update': update,
        'rating_value': existing_feedback.rating if existing_feedback else None,
    }
    return render(request, 'feedback/event_feedback_form.html', context)


@login_required
def rate_organizer(request, event_id):
    """
    View for volunteers to rate event organizers.
    """
    event = get_object_or_404(Event, pk=event_id)
    organizer = event.organizer
    
    if request.user == organizer:
        messages.error(request, _('You cannot rate yourself.'))
        return redirect('events:event_detail', pk=event_id)
    
    registration = get_object_or_404(Registration, user=request.user, event=event)
    
    if not event.is_past:
        messages.error(request, _('You can only provide ratings for past events.'))
        return redirect('events:event_detail', pk=event_id)
    
    existing_rating = OrganizerRating.objects.filter(
        volunteer=request.user, 
        organizer=organizer,
        event=event
    ).first()
    update = False
    
    if existing_rating:
        update = True
        form = OrganizerRatingForm(request.POST or None, instance=existing_rating)
    else:
        form = OrganizerRatingForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        rating = form.save(commit=False)
        if not update:
            rating.volunteer = request.user
            rating.organizer = organizer
            rating.event = event
        rating.save()
        
        messages.success(
            request, 
            _('Thank you! Your rating has been submitted.') if not update else _('Your rating has been updated.')
        )
        return redirect('events:event_detail', pk=event_id)
    
    context = {
        'form': form,
        'event': event,
        'organizer': organizer,
        'update': update,
        'rating_value': existing_rating.rating if existing_rating else None,
    }
    return render(request, 'feedback/organizer_rating_form.html', context)


@login_required
def rate_volunteer(request, event_id, volunteer_id):
    """
    View for organizers to rate volunteers who participated in their events.
    """
    event = get_object_or_404(Event, pk=event_id)
    volunteer = get_object_or_404(User, pk=volunteer_id)
    
    if request.user != event.organizer:
        messages.error(request, _('Only the event organizer can rate volunteers.'))
        return redirect('events:event_detail', pk=event_id)
    
    if request.user == volunteer:
        messages.error(request, _('You cannot rate yourself.'))
        return redirect('events:event_detail', pk=event_id)
    
    registration = get_object_or_404(Registration, user=volunteer, event=event)
    
    if not event.is_past:
        messages.error(request, _('You can only provide ratings for past events.'))
        return redirect('events:event_detail', pk=event_id)
    
    existing_rating = VolunteerRating.objects.filter(
        organizer=request.user, 
        volunteer=volunteer,
        event=event
    ).first()
    update = False
    
    if existing_rating:
        update = True
        form = VolunteerRatingForm(request.POST or None, instance=existing_rating)
    else:
        form = VolunteerRatingForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        rating = form.save(commit=False)
        if not update:
            rating.organizer = request.user
            rating.volunteer = volunteer
            rating.event = event
        rating.save()
        
        messages.success(
            request, 
            _('Thank you! Your rating has been submitted.') if not update else _('Your rating has been updated.')
        )
        return redirect('events:event_detail', pk=event_id)
    
    context = {
        'form': form,
        'event': event,
        'volunteer': volunteer,
        'update': update,
        'rating_value': existing_rating.rating if existing_rating else None,
    }
    return render(request, 'feedback/volunteer_rating_form.html', context)


@login_required
def user_ratings(request, user_id=None):
    """
    View to display all ratings for a user (either as organizer or volunteer).
    If no user_id is provided, show current user's ratings.
    """
    if user_id:
        user_profile = get_object_or_404(User, pk=user_id)
    else:
        user_profile = request.user
    
    if user_profile.role == User.Role.ORGANIZER:
        ratings = OrganizerRating.objects.filter(organizer=user_profile)
        rating_type = 'organizer'
    else:
        ratings = VolunteerRating.objects.filter(volunteer=user_profile)
        rating_type = 'volunteer'
    
    rating_stats = ratings.aggregate(
        avg_rating=Avg('rating'),
        rating_count=Count('id')
    )
    
    context = {
        'user_profile': user_profile,
        'recent_ratings': ratings.order_by('-created_at')[:10],
        'rating_type': rating_type,
        'avg_rating': rating_stats['avg_rating'] or 0,
        'rating_count': rating_stats['rating_count'] or 0,
    }
    return render(request, 'feedback/user_ratings_summary.html', context)