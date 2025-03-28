from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Event, Registration


class EventForm(forms.ModelForm):
    """
    Form for creating and updating events.
    """
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date', 'location', 'capacity', 'status']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # If this is a new event, set the default status to active
        if not self.instance.pk:
            self.fields['status'].initial = Event.Status.ACTIVE


class EventFilterForm(forms.Form):
    """
    Form for filtering events by various criteria.
    """
    search = forms.CharField(
        required=False,
        label=_("Search"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Search by title, description or location'),
            'class': 'form-control mb-2'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label=_("All Categories"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', _('All Statuses'))] + list(Event.Status.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        label=_("From Date"),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        label=_("To Date"),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    available_spots = forms.BooleanField(
        required=False,
        label=_("Only show events with available spots"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    organizer = forms.CharField(
        required=False,
        label=_("Organizer"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Filter by organizer name'),
            'class': 'form-control'
        })
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('date', _('Date (soonest first)')),
            ('-date', _('Date (latest first)')),
            ('title', _('Title (A-Z)')),
            ('-title', _('Title (Z-A)')),
            ('capacity', _('Capacity (lowest first)')),
            ('-capacity', _('Capacity (highest first)')),
        ],
        required=False,
        initial='date',
        label=_("Sort by"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super(EventFilterForm, self).__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all().order_by('name')


class RegistrationForm(forms.ModelForm):
    """
    Form for registering to an event.
    """
    class Meta:
        model = Registration
        fields = []  # No fields needed, just user and event from view
