from django import forms

from .models import Booking, Campus, Refreshments, Facility_Category
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
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        to_field_name='id'
    )
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    capacity = forms.IntegerField()

    facilities = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'required': False}),
        choices=[(facility.id, facility.title) for facility in Facility.objects.all()]
    )

class BookUpdateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        label='Meeting Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    date_start = forms.DateTimeField(
        label='Starting Date',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'id': 'datetimepicker'}))
    date_end = forms.DateTimeField(
        label='Ending Date',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'id': 'datetimepicker2'}))

    refreshments = forms.MultipleChoiceField(
        label='Refreshments',
        widget=forms.CheckboxSelectMultiple,
        choices=[(item.id, item.title) for item in Refreshments.objects.all()]
    )

    class Meta:
        model = Booking
        fields = ['title', 'date_start', 'date_end', 'refreshments']


class EditBookingForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    date_start = forms.DateTimeField()
    date_end = forms.DateTimeField()

    facilities = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(item.id, item.title) for item in Refreshments.objects.all()]
    )
