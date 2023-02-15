from django.contrib.auth.forms import UserCreationForm
from django import forms
from room_booking_app.models import User, Roles, Facility, Rooms


class CreateUserAccount(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class create_user(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    role = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(role.id, role.role_name) for role in Roles.objects.all()]
    )


class peripheralUpdate(forms.Form):
    title = forms.CharField(max_length=30)

    class Meta:
        model = Facility
        fields = ['title']


class suspend_room_form(forms.Form):
    suspension_reason = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Rooms
        fields = ['suspension_start', 'suspension_end', 'suspension_reason']

    def clean(self):
        cleaned_data = super().clean()
        suspension_start = cleaned_data.get("suspension_start")
        suspension_end = cleaned_data.get("suspension_end")
        if suspension_start and suspension_end and suspension_start >= suspension_end:
            raise forms.ValidationError(
                "Suspension end date must be after suspension start date."
            )