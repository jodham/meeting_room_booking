import datetime

import phonenumbers
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView

from accounts.forms import CreateUserAccount, UserUpdateForm, suspend_room_form, CategoryForm, \
    PeripheralForm, CampusForm, RefreshmentsForm
from room_booking_app.controllers import *
from room_booking_app.models import Facility, Rooms, Roles, Booking, Room_Suspension, Facility_Category, Campus, \
    Refreshments, System_Logs
from room_booking_app.models import User
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime


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
            if user.active:
                login(request, user)
                new_log = System_Logs()
                new_log.message = "User logged in to the System"
                new_log.key_word = "Login"
                new_log.user_id = request.user
                new_log.save()
                messages.add_message(request, messages.SUCCESS, 'login success', extra_tags='alert-success')
            else:
                messages.warning(request, 'account disabled contact admin')
                return render(request, 'accounts/signin.html')

            role = check_user_role(request.user)
            if role == 'administrator':
                return redirect('adminstrator_page')
            else:
                return redirect('rooms')
        else:
            messages.warning(request, 'Invalid details try again!!')
            templatename = 'accounts/signin.html'
            return render(request, templatename)
    else:
        templatename = 'accounts/signin.html'
        return render(request, templatename)


def signout(request):
    new_log = System_Logs()
    new_log.message = "User logged out to the System"
    new_log.key_word = "Logout"
    new_log.user_id = request.user
    new_log.save()
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
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    users = User.objects.all()
    user_roles = [(user, check_user_role(user)) for user in users]
    template_name = 'adminstrator/users.html'
    context = {'user_roles': user_roles, 'role': role}
    return render(request, template_name, context)


"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = [get_role_name(user.role) for user in self.object_list]
        return context
"""


def user_detail(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    user_id = User.objects.get(id=pk)
    templatename = 'adminstrator/user-detail.html'
    context = {'user_id': user_id, 'role': role}
    return render(request, templatename, context)


def add_user(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    available_users = User.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        parsed_number = phonenumbers.parse(phone, "KE")
        if not email.endswith('@zetech.ac.ke'):
            messages.warning(request, f'Invalid email, email must end with .@zetech.ac.ke')

        elif not phonenumbers.is_valid_number(parsed_number):
            messages.warning(request, f'invalid phonenumber check')
        elif available_users.filter(email=email).exists():
            messages.warning(request, f'user with that email already exists')
        elif password1 != password2:
            messages.warning(request, f'Passwords do not match, Please check')
        else:
            user = User.objects.create_user(email=email, password=password1, first_name=first_name,
                                            last_name=last_name, phone_number=phone)
            messages.success(request, f'User created successfully!')
            return redirect('system_users')
    templatename = 'accounts/register.html'
    return render(request, templatename, {'role': role})


def update_user(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
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
        messages.add_message(request, messages.SUCCESS, 'user updated successfully', extra_tags='alert-success')
        return redirect('system_users')

    form.fields['email'].initial = user.email
    form.fields['first_name'].initial = user.first_name
    form.fields['last_name'].initial = user.last_name
    form.fields['role'].initial = role_ids

    return render(request, 'adminstrator/update_user.html', {'form': form, 'roles': roles, 'role': role, 'user': user})


def activate_deactivate_user(request, id):
    if not (request.user.is_authenticated and request.user.is_admin):
        return redirect('signin')
    user = get_object_or_404(User, id=id)
    if user.active:
        user.active = False
        user.save()
        print(timezone.localtime())
        messages.add_message(request, messages.SUCCESS, 'user has been deactivated', extra_tags='alert-success')
        return redirect('system_users')
    else:
        user.active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'user has been activated', extra_tags='alert-success')
        return redirect('system_users')


def system_logs(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    logs = System_Logs.objects.all()
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
    form = PeripheralForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('peripherals')
    else:
        form = PeripheralForm()
    templatename = 'adminstrator/create_peripheral.html'
    return render(request, templatename, {'role': role, 'form': form})


class PeripheralUpdateView(UpdateView):
    model = Facility
    form_class = PeripheralForm
    template_name = 'adminstrator/peripheral_update.html'
    success_url = reverse_lazy('peripherals')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # You can add any extra logic here to customize how the object is retrieved
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            role = check_user_role(self.request.user)
        else:
            role = None
        context['role'] = role
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Peripheral updated successfully.')
        return response


def activate_deactivate_peripheral(request, pk):
    if not request.user.is_admin:
        return redirect(signin)
    peripheral = get_object_or_404(Facility, id=pk)
    if peripheral.active:
        peripheral.active = False
        messages.add_message(request, messages.SUCCESS, f'peripheral is deactivated', extra_tags='alert-success')
        peripheral.save()
        return redirect('peripherals')
    else:
        peripheral.active = True
        messages.add_message(request, messages.SUCCESS, 'peripheral is activated', extra_tags='alert-success')
        peripheral.save()
        return redirect('peripherals')


# --------------------------rooms/facilities---------------
def activate_deactivate_room(request, pk):
    if not request.user.is_admin:
        return redirect(signin)
    room = get_object_or_404(Rooms, id=pk)
    if room.is_active:
        room.is_active = False
        messages.add_message(request, messages.SUCCESS, 'room has been deactivated', extra_tags='alert-success')
        room.save()
        return redirect('dashboard')
    else:
        room.is_active = True
        messages.add_message(request, messages.SUCCESS, 'room has been activated', extra_tags='alert-success')
        room.save()
        return redirect('dashboard')


# -----------------approve booking --------------------------

def approve_booking(request, pk):
    if not request.user.is_authenticated:
        return redirect('signin')
    booking = get_object_or_404(Booking, id=pk)
    user = User.objects.get(email=request.user)
    if booking.status == 0 or booking.status == 2:
        booking.status = 1
        booking.actioned_by = user
        booking.date_actioned = timezone.now()
        booking.save()
        messages.success(request, f'booking is approved')
        return redirect('booking_detail', pk=pk)


def cancel_booking(request, pk):
    if not request.user.is_authenticated:
        return redirect('sign')
    booking = get_object_or_404(Booking, id=pk)
    user = User.objects.get(email=request.user)
    if booking.status == 0 or booking.status == 1 or booking.status == 2:
        booking.status = 3
        booking.actioned_by = user
        booking.date_actioned = timezone.now()
        booking.save()
        messages.success(request, f'booking is cancelled')
        return redirect('booking_detail', pk=pk)


def reject_booking(request, pk):
    if not request.user.is_authenticated:
        return redirect('sign')
    booking = get_object_or_404(Booking, id=pk)
    user = User.objects.get(email=request.user)
    if booking.status == 0 or booking.status == 1:
        booking.status = 2
        booking.actioned_by = user
        booking.date_actioned = timezone.now()
        booking.save()
        messages.success(request, f'booking is rejected')
        return redirect('booking_detail', pk=pk)


def suspend_room(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    room = get_object_or_404(Rooms, id=pk)
    user = User.objects.get(email=request.user)
    if request.method == "POST":
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        reason = request.POST.get('reason')

        suspension_starting_time = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M")

        if suspension_starting_time < datetime.datetime.now():
            messages.error(request, 'Start time must be greater than current time.')
            return redirect('suspend_room', pk)

        elif end_date < start_date:
            messages.warning(request, 'ending time cannot be less than starting time')
            return redirect('suspend_room', pk)

        x = Room_Suspension()
        x.room = room
        x.start_date = start_date
        x.end_date = end_date
        x.user = user
        x.suspension_reason = reason
        x.is_suspended = True
        x.save()
        return redirect('room_detail', pk=pk)
    else:
        form = suspend_room_form()
    templatename = 'adminstrator/suspend_room.html'
    context = {'role': role, 'room': room, 'form': form}
    return render(request, templatename, context)


def add_facility_category(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    if request.method == "POST":
        title = request.POST.get('title')
        new_category = Facility_Category()
        new_category.title = title
        new_category.save()
        return redirect('facility_category')
    templatename = 'adminstrator/add_category.html'
    context = {'role': role}
    return render(request, templatename, context)


def edit_facility_category(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    category = get_object_or_404(Facility_Category, pk=pk)

    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, f'category edited susccessfully')
        return redirect('facility_category')

    else:
        form = CategoryForm(instance=category)

    templatename = 'adminstrator/edit_category.html'
    context = {'form': form, 'category': category, 'role': role}
    return render(request, templatename, context)


def facility_category(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    categories = Facility_Category.objects.all()
    templatename = 'adminstrator/facility_categories.html'
    context = {'categories': categories, 'role': role}
    return render(request, templatename, context)


def add_campus(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    form = CampusForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, f'successfully added a campus')
        return redirect('campus_list')
    else:
        form = CampusForm()

    templatename = 'adminstrator/add_campus.html'
    context = {'form': form, 'role': role}
    return render(request, templatename, context)


def Campuses(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    campuses = Campus.objects.all()
    templatename = 'adminstrator/campuses.html'
    context = {'campuses': campuses, 'role': role}
    return render(request, templatename, context)


class CampusUpdateView(UpdateView):
    model = Campus
    form_class = CampusForm
    template_name = 'adminstrator/campus_update.html'
    success_url = reverse_lazy('campus_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # You can add any extra logic here to customize how the object is retrieved
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            role = check_user_role(self.request.user)
        else:
            role = None
        context['role'] = role
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Campus edited successfully.')
        return response


def Refreshments_View(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    refreshments = Refreshments.objects.all()
    templatename = 'adminstrator/refreshments_list.html'
    context = {'refreshments': refreshments, 'role': role}
    return render(request, templatename, context)


def Add_refreshment(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    form = RefreshmentsForm(request.POST or None)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        form.save()
        messages.success(request, f'successsfully added refreshment {title}')
        return redirect('refreshments_list')
    else:
        form = RefreshmentsForm()
    templatename = 'adminstrator/add_refreshment.html'
    context = {'form': form, 'role': role}
    return render(request, templatename, context)


def edit_refreshment(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    refreshment = get_object_or_404(Refreshments, pk=pk)
    form = RefreshmentsForm(request.POST, instance=refreshment)
    if form.is_valid():
        form.save()
        messages.success(request, f'succefully edited refreshment')
        return redirect('refreshments_list')
    else:
        form = RefreshmentsForm(instance=refreshment)
    templatename = 'adminstrator/edit_refreshment.html'
    context = {'form': form, 'role': role}
    return render(request, templatename, context)


def user_profile(request, user_id, room_id):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    user = get_object_or_404(User, pk=user_id)
    room = get_object_or_404(Rooms, pk=room_id)
    context = {'user': user, 'role': role, 'room': room}
    templatename = 'accounts/profile.html'
    return render(request, templatename, context)


def reports(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    context = {'role': role}
    templatename = 'accounts/reports.html'
    return render(request, templatename, context)


from django.shortcuts import get_object_or_404


def usage_report(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None

    bookings = Booking.objects.all()
    users = User.objects.all()
    all_peripherals = Facility.objects.all()
    refreshments = Refreshments.objects.all()
    rooms = Rooms.objects.all()

    if request.method == 'POST':
        selected_user_id = request.POST.get('user')
        facility_id = request.POST.get('facility')
        peripheral_id = request.POST.get('peripheral')
        refreshment_id = request.POST.get('refreshment')
        datefrom = request.POST.get('datefrom')
        dateto = request.POST.get('dateto')

        if all([selected_user_id, facility_id, peripheral_id, refreshment_id, datefrom, dateto]):
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_peripheral = int(peripheral_id)
            selected_refreshment = int(refreshment_id)
            selected_from_date = datefrom
            selected_date_to = dateto
            user = get_object_or_404(User, id=selected_user_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room=facility_id,
                date_from__gte=datetime.strptime(datefrom, '%Y-%m-%d').date(),
                date_to__lte=datetime.strptime(dateto, '%Y-%m-%d').date()
            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            ).filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )

            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral': selected_peripheral,
                'selected_refreshment': selected_refreshment,
                'selected_from_date': selected_from_date,
                'selected_date_to': selected_date_to
            }
            return render(request, 'accounts/usage_report.html', context)
        elif all([selected_user_id, facility_id, peripheral_id, refreshment_id, datefrom]):
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_refreshment = int(refreshment_id)
            selected_peripheral = int(peripheral_id)
            selected_from_date = datefrom
            user = get_object_or_404(User, id=selected_user_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room_id=facility_id,
                date_start__gte=datetime.strptime(datefrom, '%Y-%m-%d').date(),
            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            ).filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )
            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral_id': selected_peripheral,
                'selected_refreshment': selected_refreshment,
                'selected_from_date': selected_from_date,
            }
            return render(request, 'accounts/usage_report.html', context)

        elif all([selected_user_id, facility_id, peripheral_id, refreshment_id]):
            user = get_object_or_404(User, id=selected_user_id)
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_refreshment = int(refreshment_id)
            selected_peripheral = int(peripheral_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room_id=facility_id,

            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            ).filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )
            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral': selected_peripheral,
                'selected_refreshment': selected_refreshment

            }
            return render(request, 'accounts/usage_report.html', context)
        elif all([selected_user_id, facility_id, peripheral_id]):
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_peripheral = int(peripheral_id)
            user = get_object_or_404(User, id=selected_user_id)

            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room_id=facility_id,
            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            )
            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral': selected_peripheral,
            }
            return render(request, 'accounts/usage_report.html', context)
        # -----------------------user and facility------------------------>
        elif selected_user_id and facility_id:
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            user = get_object_or_404(User, id=selected_user_id)
            facility = get_object_or_404(Rooms, id=facility_id)
            bookings = Booking.objects.filter(Q(user_id=user) & Q(room_id=facility))

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'peripheral_id': peripheral_id,
                'refreshment_id': refreshment_id

            }

            return render(request, 'accounts/usage_report.html', context)
        elif selected_user_id:
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            bookings = Booking.objects.filter(user_id=selected_user_id)
            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'peripheral_id': peripheral_id,
                'refreshment_id': refreshment_id
            }

            return render(request, 'accounts/usage_report.html', context)
        elif all([facility_id]):
            facility = get_object_or_404(Rooms, id=facility_id)
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            bookings = Booking.objects.filter(room_id=facility)

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'peripheral_id': peripheral_id,
                'refreshment_id': refreshment_id
            }

            return render(request, 'accounts/usage_report.html', context)
        elif peripheral_id:
            selected_peripheral = int(peripheral_id)
            bookings = Booking.objects.filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            )

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_peripheral': selected_peripheral,
                'refreshment_id': refreshment_id
            }

            return render(request, 'accounts/usage_report.html', context)
        elif refreshment_id:
            selected_refreshment = int(refreshment_id)
            bookings = Booking.objects.filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'peripheral_id': peripheral_id,
                'selected_refreshment': selected_refreshment

            }

            return render(request, 'accounts/usage_report.html', context)
    peripheral_names = None
    for booking in bookings:
        if booking.extra_peripherals:
            peripheral_ids = set(booking.extra_peripherals.split(','))
            peripherals = Facility.objects.filter(id__in=peripheral_ids)
            if peripherals.exists():
                peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                booking.peripheral_names = peripheral_names
            else:
                booking.peripheral_names = ""
        else:
            booking.peripheral_names = ""

    refreshment_names = None
    for booking in bookings:
        if booking.refreshments:
            refreshment_ids = set(booking.refreshments.split(','))
            refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
            if refreshments.exists():
                refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                booking.refreshment_names = refreshment_names
            else:
                booking.refreshment_names = ""
        else:
            booking.refreshment_names = ""

    context = {
        'users': users,
        'all_peripherals': all_peripherals,
        'refreshments': refreshments,
        'rooms': rooms,
        'bookings': bookings,
        'peripheral_names': peripheral_names,
        'refreshment_names': refreshment_names,
        'role': role
    }

    return render(request, 'accounts/usage_report.html', context)


def summary_report(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    total_users = User.objects.all().count()
    total_active_users = User.objects.all().filter(active=True).count()
    total_facilities = Rooms.objects.all().count()
    total_active_facilities = Rooms.objects.all().filter(is_active=True).count()
    total_peripherals = Facility.objects.all().count()
    total_active_peripherals = Facility.objects.all().filter(active=True).count()
    total_refreshments = Refreshments.objects.all().count()
    templatename = 'accounts/summary_report.html'
    context = {'role': role, 'total_users': total_users, 'total_facilities': total_facilities,
               'total_active_facilities': total_active_facilities,
               'total_peripherals': total_peripherals, 'total_refreshments': total_refreshments,
               'total_active_users': total_active_users,
               'total_active_peripherals': total_active_peripherals}
    return render(request, templatename, context)
