from django.contrib.auth.forms import UserCreationForm
from django import forms
from room_booking_app.models import User, Roles, Facility, Rooms, Facility_Category, Campus


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
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True})
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})

    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    role = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'required': True}),
        choices=[(role.id, role.role_name) for role in Roles.objects.all()]
    )


class PeripheralForm(forms.ModelForm):
    title = forms.CharField(
        label='Peripheral Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    category = forms.ModelChoiceField(
        label='Category Title',
        queryset=Facility_Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Facility
        fields = ('title', 'category')


class peripheralUpdate(forms.Form):
    title = forms.CharField(max_length=30)

    class Meta:
        model = Facility
        fields = ['title']


class suspend_room_form(forms.Form):
    suspension_reason = forms.CharField(max_length=200, required=True)
    suspension_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    suspension_end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Rooms
        fields = ['suspension_start', 'suspension_end', 'suspension_reason']

    def clean(self):
        cleaned_data = super().clean()
        suspension_start = cleaned_data.get("suspension_start")
        suspension_end = cleaned_data.get("suspension_end")
        if suspension_start and suspension_end and suspension_start >= suspension_end:
            self.add_error('suspension_end',
                           "Suspension end date must be after suspension start date."
                           )


class CategoryForm(forms.ModelForm):
    title = forms.CharField(
        label='Category Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )

    class Meta:
        model = Facility_Category
        fields = ('title',)


class CampusForm(forms.ModelForm):
    title = forms.CharField(
        label='Campus Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )

    class Meta:
        model = Campus
        fields = ('title',)
