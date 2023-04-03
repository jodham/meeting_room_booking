from django import forms

from .models import Booking, Campus, Refreshments, Facility_Category
from .models import Facility


class RoomForm(forms.Form):
    Location = forms.ModelChoiceField(
        queryset=Campus.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        to_field_name='id'
    )
    Title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    Capacity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    Peripherals = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'required': False}),
        choices=[(facility.id, facility.title) for facility in Facility.objects.all()]
    )


class UpdateBookingForm(forms.Form):
    Purpose = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    Starting_Date = forms.CharField(
        label='Starting Date',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datetimepicker'}))
    Ending_Date = forms.CharField(
        label='Ending Date',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datetimepicker2'}))

    refreshments = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'required': False}),
        choices=[(refreshment.id, refreshment.title) for refreshment in Refreshments.objects.all()]
    )
    extra_peripherals = forms.MultipleChoiceField(
        widget=forms.TextInput(attrs={'required': False}),
        choices=[(peripheral.id, peripheral.title) for peripheral in Facility.objects.all()]
    )


class BookUpdateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        label='Meeting Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    date_start = forms.CharField(
        label='Starting Date',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datetimepicker'}))
    date_end = forms.CharField(
        label='Ending Date',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datetimepicker2'}))

    extra_peripherals = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    refreshments = forms.ModelMultipleChoiceField(
        queryset=Refreshments.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Booking
        fields = ['title', 'date_start', 'date_end', 'extra_peripherals', 'refreshments']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     booking = self.instance
    #
    #     available_peripherals = Facility.objects.filter(active=True)
    #     available_refreshments = Refreshments.objects.all()
    #
    #     self.fields['extra_peripherals'].queryset = available_peripherals
    #     self.fields['refreshments'].queryset = available_refreshments
    #
    #     extra_peripheral_ids = []
    #     if booking.extra_peripherals:
    #         if isinstance(booking.extra_peripherals, str):
    #             extra_peripheral_ids = [int(pk) for pk in booking.extra_peripherals.split(',') if pk]
    #         else:
    #             extra_peripheral_ids = list(booking.extra_peripherals.values_list('id', flat=True))
    #     initial_extra_peripheral_ids = available_peripherals.filter(id__in=extra_peripheral_ids).values_list('id',
    #                                                                                                          flat=True)
    #     self.fields['extra_peripherals'].initial = initial_extra_peripheral_ids
    #
    #     refreshments_ids = []
    #     if booking.refreshments:
    #         if isinstance(booking.refreshments, str):
    #             refreshments_ids = [int(pk) for pk in booking.refreshments.split(',') if pk]
    #         else:
    #             refreshments_ids = list(booking.refreshments.values_list('id', flat=True))
    #     initial_refreshments = available_refreshments.filter(id__in=refreshments_ids)
    #     self.fields['refreshments'].initial = initial_refreshments


class Edit_booking_form(forms.Form):
    Purpose = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    extra_peripherals = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'required': False}),
        choices=[(peripheral.id, peripheral.title) for peripheral in Facility.objects.all()]
    )
    Starting_Date = forms.CharField(
        label='Starting Date',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datetimepicker'}))

    refreshments = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'required': False}),
        choices=[(refreshment.id, refreshment.title) for refreshment in Refreshments.objects.all()]
    )
    Ending_Date = forms.CharField(
        label='Ending Date',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'datetimepicker2'}))
