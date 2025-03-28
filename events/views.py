from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.utils.timezone import now

from .models import Event, Registration, Category
from .forms import EventForm, EventFilterForm, RegistrationForm
from .services import send_registration_confirmation_email, send_registration_cancellation_email


class EventListView(ListView):
    """
    View for displaying a list of all active events.
    """
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Event.objects.select_related('category', 'organizer').all()
        
        # Apply filters from the form
        form = EventFilterForm(self.request.GET)
        if form.is_valid():
            # Search functionality
            if form.cleaned_data.get('search'):
                search_query = form.cleaned_data['search']
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(location__icontains=search_query)
                )
            
            # Filter by category
            if form.cleaned_data.get('category'):
                queryset = queryset.filter(category=form.cleaned_data['category'])
            
            # Filter by status
            if form.cleaned_data.get('status'):
                queryset = queryset.filter(status=form.cleaned_data['status'])
            
            # Filter by date range
            if form.cleaned_data.get('date_from'):
                queryset = queryset.filter(date__gte=form.cleaned_data['date_from'])
            
            if form.cleaned_data.get('date_to'):
                queryset = queryset.filter(date__lte=form.cleaned_data['date_to'])
                
            # Filter by available spots
            if form.cleaned_data.get('available_spots'):
                for event in queryset:
                    if event.available_spots <= 0:
                        queryset = queryset.exclude(id=event.id)
            
            # Filter by organizer name
            if form.cleaned_data.get('organizer'):
                organizer_query = form.cleaned_data['organizer']
                queryset = queryset.filter(
                    Q(organizer__first_name__icontains=organizer_query) |
                    Q(organizer__last_name__icontains=organizer_query) |
                    Q(organizer__username__icontains=organizer_query)
                )
            
            # Sort results
            if form.cleaned_data.get('sort_by'):
                queryset = queryset.order_by(form.cleaned_data['sort_by'])
            else:
                # Default sorting
                queryset = queryset.order_by('status', '-date')
        else:
            # Default to showing active events first
            queryset = queryset.order_by('status', '-date')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = EventFilterForm(self.request.GET or None)
        context['active_events_count'] = Event.objects.filter(status=Event.Status.ACTIVE).count()
        context['total_events_count'] = Event.objects.count()
        # Get filter params for pagination links
        if self.request.GET:
            context['filter_params'] = '&'.join([f"{key}={value}" for key, value in self.request.GET.items() if key != 'page'])
        else:
            context['filter_params'] = ''
        return context


class EventDetailView(DetailView):
    """
    View for displaying details of a specific event.
    """
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if current user is registered for this event
        if self.request.user.is_authenticated:
            context['is_registered'] = Registration.objects.filter(
                user=self.request.user,
                event=self.object
            ).exists()
        return context


class OrganizerRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure the user has organizer role.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_organizer()


class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    """
    View for creating a new event (only for organizers).
    """
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing event (only for the organizer who created it).
    """
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def test_func(self):
        event = self.get_object()
        return (self.request.user.is_organizer() and 
                self.request.user == event.organizer)
    
    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully!')
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting an event (only for the organizer who created it).
    """
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')
    context_object_name = 'event'
    
    def test_func(self):
        event = self.get_object()
        return (self.request.user.is_organizer() and 
                self.request.user == event.organizer)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def register_for_event(request, pk):
    """
    View for registering a user to an event.
    """
    event = get_object_or_404(Event, pk=pk)
    
    # Check if event is active
    if event.status != Event.Status.ACTIVE:
        messages.error(request, 'Registration is not available for this event.')
        return redirect('events:event_detail', pk=pk)
    
    # Check if event is full
    if event.registered_count >= event.capacity:
        messages.error(request, 'This event is already at full capacity.')
        return redirect('events:event_detail', pk=pk)
    
    # Check if user is already registered
    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.info(request, 'You are already registered for this event.')
        return redirect('events:event_detail', pk=pk)
    
    # Check if user has an email set
    if not request.user.email:
        messages.warning(
            request, 
            'Please update your email address in your profile to receive confirmation emails.'
        )
    
    # Register the user
    registration = Registration(user=request.user, event=event)
    registration.save()
    
    # Send confirmation email
    if request.user.email:
        try:
            send_registration_confirmation_email(request.user, event)
        except Exception as e:
            messages.warning(
                request, 
                'Registration successful, but there was an error sending the confirmation email.'
            )
    
    messages.success(request, 'You have successfully registered for this event!')
    return redirect('events:event_detail', pk=pk)


@login_required
def cancel_registration(request, pk):
    """
    View for canceling a user's registration to an event.
    """
    event = get_object_or_404(Event, pk=pk)
    registration = get_object_or_404(Registration, user=request.user, event=event)
    
    # Only allow cancellation if the event is in the future
    if event.is_past:
        messages.error(request, 'Cannot cancel registration for past events.')
        return redirect('events:event_detail', pk=pk)
    
    # Store user before deleting registration
    user = request.user
    
    # Delete registration
    registration.delete()
    
    # Send cancellation email
    if user.email:
        try:
            send_registration_cancellation_email(user, event)
        except Exception as e:
            messages.warning(
                request, 
                'Registration canceled, but there was an error sending the cancellation email.'
            )
    
    messages.success(request, 'Your registration has been canceled.')
    return redirect('events:event_detail', pk=pk)


@login_required
def mark_attendance(request):
    """
    View for marking a participant's attendance for an event.
    Only event organizers can mark attendance.
    """
    if request.method != 'POST':
        return redirect('events:event_list')
    
    registration_id = request.POST.get('registration_id')
    if not registration_id:
        messages.error(request, 'Invalid request.')
        return redirect('events:event_list')
    
    registration = get_object_or_404(Registration, pk=registration_id)
    event = registration.event
    
    # Only the event organizer can mark attendance
    if request.user != event.organizer:
        messages.error(request, 'You do not have permission to mark attendance for this event.')
        return redirect('events:event_detail', pk=event.id)
    
    # Toggle attendance status
    registration.attended = not registration.attended
    registration.save()
    
    messages.success(
        request, 
        f'Attendance for {registration.user.get_full_name() or registration.user.username} has been updated.'
    )
    return redirect('events:event_detail', pk=event.id)
