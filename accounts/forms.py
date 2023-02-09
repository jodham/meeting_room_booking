from django.contrib.auth.forms import UserCreationForm
from django import forms
from room_booking_app.models import User, Roles


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
