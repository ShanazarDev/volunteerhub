from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration with additional fields for the custom User model.
    """
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.RadioSelect,
        initial=User.Role.VOLUNTEER,
        help_text=_('Select your role in the VolunteerHub')
    )
    
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text=_('Tell us a bit about yourself')
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        help_text=_('Your contact phone number')
    )
    
    telegram_username = forms.CharField(
        max_length=100,
        required=False,
        help_text=_('Your Telegram username for notifications')
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 
                  'bio', 'phone', 'telegram_username', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with bootstrap styling.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'phone', 'telegram_username')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
