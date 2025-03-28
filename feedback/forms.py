from django import forms
from django.utils.translation import gettext_lazy as _

from .models import EventFeedback, OrganizerRating, VolunteerRating


class RatingForm(forms.Form):
    """
    Base form for all rating forms. Contains common fields and validation.
    """
    rating = forms.IntegerField(
        label=_('Rating (1-5 stars)'),
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.HiddenInput(attrs={'class': 'rating-value'})
    )
    comment = forms.CharField(
        label=_('Comment (optional)'),
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': _('Share your thoughts and feedback...')
        })
    )


class EventFeedbackForm(forms.ModelForm):
    """
    Form for users to provide feedback for events they attended.
    """
    class Meta:
        model = EventFeedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(attrs={'class': 'rating-value'}),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': _('Share your thoughts about this event...')
            })
        }


class OrganizerRatingForm(forms.ModelForm):
    """
    Form for volunteers to rate event organizers.
    """
    class Meta:
        model = OrganizerRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(attrs={'class': 'rating-value'}),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': _('Share your thoughts about this organizer...')
            })
        }


class VolunteerRatingForm(forms.ModelForm):
    """
    Form for organizers to rate volunteers.
    """
    class Meta:
        model = VolunteerRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(attrs={'class': 'rating-value'}),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': _('Share your thoughts about this volunteer...')
            })
        }