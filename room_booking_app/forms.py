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

    extra_peripherals = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    refreshments = forms.ModelMultipleChoiceField(
        queryset=Refreshments.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        booking = self.instance

        available_peripherals = Facility.objects.filter(active=True)
        available_refreshments = Refreshments.objects.all()

        self.fields['extra_peripherals'].queryset = available_peripherals
        self.fields['refreshments'].queryset = available_refreshments

        extra_peripheral_ids = []
        if booking.extra_peripherals:
            if isinstance(booking.extra_peripherals, str):
                extra_peripheral_ids = [int(pk) for pk in booking.extra_peripherals.split(',') if pk]
            else:
                extra_peripheral_ids = list(booking.extra_peripherals.values_list('id', flat=True))
        self.fields['extra_peripherals'].initial = available_peripherals.filter(id__in=extra_peripheral_ids)

        if not extra_peripheral_ids:
            self.fields['extra_peripherals'].initial = None

        refreshments_ids = []
        if booking.refreshments:
            if isinstance(booking.refreshments, str):
                refreshments_ids = [int(pk) for pk in booking.refreshments.split(',') if pk]
            else:
                refreshments_ids = list(booking.refreshments.value_list('id', flat=True))
            self.fields['refreshments'].initial = available_refreshments.filter(id__in=refreshments_ids)
        if not refreshments_ids:
            self.fields['refreshments'].initial = None

    class Meta:
        model = Booking
        fields = ['title', 'date_start', 'date_end', 'extra_peripherals', 'refreshments']


class EditBookingForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    date_start = forms.DateTimeField()
    date_end = forms.DateTimeField()

    facilities = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(item.id, item.title) for item in Refreshments.objects.all()]
    )
