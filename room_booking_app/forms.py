from django import forms

from .models import Booking, Campus
from .models import Facility


class BookingForm(forms.ModelForm):
    starting_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    ending_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    room_id = forms.CharField(widget=forms.HiddenInput())
    booked_by = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Booking
        fields = ('title', 'starting_time', 'ending_time')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        room_id = kwargs.pop('room_id', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['room_id'].initial = room_id


class RoomForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        widget=forms.Select,
        to_field_name='id'
    )
    title = forms.CharField(max_length=100)
    capacity = forms.IntegerField()

    facilities = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(facility.id, facility.title) for facility in Facility.objects.all()]
    )


class BookUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    date_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    date_end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ['title', 'date_start', 'date_end']
