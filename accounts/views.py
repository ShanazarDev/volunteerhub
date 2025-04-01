from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import User


class RegisterView(CreateView):
    """
    View for user registration. Creates a new User object.
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """Log in the user after successful registration."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    """
    Custom login view with our styled form.
    """
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    """
    View for updating user profile information.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        """Return the current logged-in user."""
        return self.request.user
        
    def form_valid(self, form):
        """Add success message after successful profile update."""
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)


@login_required
def profile_view(request):
    """
    Display user profile information and event participation history.
    """
    user = request.user
    registered_events = user.registrations.all().order_by('-event__date')
    
    if user.is_organizer():
        organized_events = user.events_created.all().order_by('-date')
    else:
        organized_events = None
    
    context = {
        'user': user,
        'registered_events': registered_events,
        'organized_events': organized_events,
    }
    
    return render(request, 'accounts/profile.html', context)