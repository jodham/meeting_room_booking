from django import forms
from .models import Booking
from django import forms
from .models import Rooms, Facility


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


class RoomForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['location', 'title', 'capacity', 'facilities_ids']

    facilities_ids = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
