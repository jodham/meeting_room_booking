from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.admin.models import LogEntry
from room_booking_app.controllers import *
from accounts.forms import CreateUserAccount, create_user, UserUpdateForm
from room_booking_app.models import User, Facility, Rooms, Roles, Booking


# Create your views here.
def register(request):
    if request.method == "POST":
        form = CreateUserAccount(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'account created successfully')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('dashboard')
    else:
        form = CreateUserAccount()
    templatename = 'accounts/register.html'
    context = {'form': form}
    return render(request, templatename, context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            role = check_user_role(request.user)
            if role == 'administrator':
                return redirect('adminstrator_page')
            else:
                return redirect('dashboard')
        else:
            error = messages.error(request, 'Invalid details try again!!')
            templatename = 'accounts/signin.html'
            context = {"error": error}
            return render(request, templatename, context)
    else:
        templatename = 'accounts/signin.html'
        return render(request, templatename)



def signout(request):
    logout(request)
    return redirect('signin')


# -------------------Admin--page---------------------

def adminstrator(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    templatename = 'accounts/adminstrator_panel.html'
    context = {'role': role}
    return render(request, templatename, context)


# ------------------------ListView-------------------------
def UsersListView(request):
    users = User.objects.all()
    user_roles = [(user, check_user_role(user)) for user in users]
    template_name = 'adminstrator/users.html'
    context = {'user_roles': user_roles}
    return render(request, template_name, context)


"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = [get_role_name(user.role) for user in self.object_list]
        return context
"""


def user_detail(request, pk):
    user_id = User.objects.get(id=pk)
    templatename = 'adminstrator/user-detail.html'
    context = {'user_id': user_id}
    return render(request, templatename, context)


def add_user(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    if request.method == 'POST':
        form = create_user(request.POST)
        if form.is_valid():
            form.save()
            return redirect('system_users')
    else:
        form = create_user()
        messages.error(request, "wrong user details")
    templatename = 'accounts/register.html'
    return render(request, templatename, {'form': form,'role': role})


def update_user(request, pk):
    user = get_object_or_404(User, id=pk)
    role_ids = user.role.split(',')
    roles = Roles.objects.all()
    form = UserUpdateForm(request.POST or None)
    if form.is_valid():
        user.email = form.cleaned_data.get('email')
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        selected_roles = form.cleaned_data.get('role')

        user.role = ','.join(selected_roles)
        user.save()
        return redirect('system_users')

    form.fields['email'].initial = user.email
    form.fields['first_name'].initial = user.first_name
    form.fields['last_name'].initial = user.last_name
    form.fields['role'].initial = role_ids

    return render(request, 'adminstrator/update_user.html', {'form': form, 'roles': roles})


def activate_deactivate_user(request, id):
    if not (request.user.is_authenticated and request.user.is_admin):
        return redirect('signin')
    user = get_object_or_404(User, id=id)
    if user.active:
        user.active = False
        user.save()
        messages.success(request, 'user has been deactivated', extra_tags="alert alert warning dismissable show")
        return redirect('system_users')
    else:
        user.active = True
        user.save()
        messages.success(request, 'user has been activated', extra_tags="alert alert warning dismissable show")
        return redirect('system_users')


def system_logs(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    logs = LogEntry.objects.all()
    templatename = 'adminstrator/system-logs.html'
    context = {'logs': logs, 'role': role}
    return render(request, templatename, context)


# -----------------------peripherals---------------------
def peripherals(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    peripheral = Facility.objects.all()
    context = {'peripheral': peripheral, 'role': role}
    return render(request, 'adminstrator/peripherals.html', context)


def create_peripheral(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    if request.method == "POST":
        title = request.POST.get('title')
        facility = Facility()
        facility.title = title
        facility.save()
        return reverse('peripherals')
    templatename = 'adminstrator/create_peripheral.html'
    return render(request, templatename, {'role': role})


class PeripheralUpdateView(UpdateView):
    model = Facility
    fields = ['title']
    success_url = 'peripherals'
    template_name = 'adminstrator/create_peripheral.html'


def activate_deactivate_peripheral(request, pk):
    if not request.user.is_admin:
        return redirect(signin)
    peripheral = get_object_or_404(Facility, id=pk)
    if peripheral.active:
        peripheral.active = False
        messages.success(request, 'peripheral is deactivated')
        peripheral.save()
        return redirect('peripherals')
    else:
        peripheral.active = True
        messages.success(request, 'peripheral is activated')
        peripheral.save()
        return redirect('peripherals')


# --------------------------rooms/facilities---------------
def activate_deactivate_room(request, pk):
    if not request.user.is_admin:
        return redirect(signin)
    room = get_object_or_404(Rooms, id=pk)
    if room.is_active:
        room.is_active = False
        messages.success(request, 'room has been deactivated', fail_silently=True)
        room.save()
        return redirect('dashboard')
    else:
        room.is_active = True
        messages.success(request, 'room has been activated', fail_silently=True)
        room.save()
        return redirect('dashboard')


# -----------------approve booking --------------------------

def approve_booking(request, pk):
    if not request.user.is_authenticated:
        return redirect('signin')
    booking = get_object_or_404(Booking, id=pk)
    if booking.status == 0 or booking.status == 2:
        booking.status = 1
        booking.save()
        return redirect('booking_detail', pk=pk)


def reject_booking(request, pk):
    if not request.user.is_authenticated:
        return redirect('sign')
    booking = get_object_or_404(Booking, id=pk)
    if booking.status == 0 or booking.status == 1:
        booking.status = 2
        booking.save()
        return redirect('booking_detail', pk=pk)
