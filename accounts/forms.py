from django.contrib.auth.forms import UserCreationForm
from django import forms
from room_booking_app.models import MyUser


class CreateUserAccount(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
