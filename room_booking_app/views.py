# from django.shortcuts import render, redirect
import datetime
from datetime import time, date, timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
# from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView

from .controllers import *
from .forms import RoomForm, BookUpdateForm, EditBookingForm
from .models import Booking, User, Room_Suspension, Refreshments, Booking_Approval
from .models import Rooms, Campus, Facility


# Create your views here.
def index(request):
    templatename = 'room_booking_app/index.html'
    context = {}
    return render(request, templatename, context)


@login_required(login_url='signin')
def dashboard(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    templatename = 'room_booking_app/rooms.html'
    suspended_rooms = Room_Suspension.objects.all()
    rooms = Rooms.objects.all().order_by('-date_created')
    context = {'rooms': rooms, 'role': role, 'suspended_rooms': suspended_rooms}
    return render(request, templatename, context)


def activeRooms(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    available_rooms = Rooms.objects.all()
    active_rooms = available_rooms.filter(is_active=True)
    templatename = 'room_booking_app/active_rooms.html'
    context = {'role': role, 'active_rooms': active_rooms}
    return render(request, templatename, context)


# ------------------------------room create view------>

def create_room_form(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    campus = Campus.objects.all()
    facility = Facility.objects.all()
    facilities = []
    if request.method == "POST":
        location_id = request.POST.get('location_id')
        campus_loc = Campus.objects.get(id=location_id)
        title = request.POST.get('title')
        capacity = request.POST.get('capacity')
        facilities_ids = ",".join(request.POST.getlist('facilities'))
        room = Rooms(location=campus_loc, title=title, capacity=capacity, facilities_ids=facilities_ids)
        room.save()
        return redirect('dashboard')
    templatename = 'room_booking_app/room_form.html'
    context = {'campus': campus, 'facility': facility, 'facilities': facilities, 'role': role}
    return render(request, templatename, context)


# ------------------------------------Update Views---------------------------->

def RoomUpdateView(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    room = Rooms.objects.get(id=pk)
    facilities_ids = room.facilities_ids.split(',')
    facilities = Facility.objects.all()
    form = RoomForm(request.POST or None)

    if form.is_valid():
        location = form.cleaned_data.get('location')
        title = form.cleaned_data.get('title')
        capacity = form.cleaned_data.get('capacity')
        selected_facilities = form.cleaned_data.get('facilities')

        room.location = location
        room.title = title
        room.capacity = capacity
        room.facilities_ids = ','.join(selected_facilities)
        room.save()
        return redirect('dashboard')

    form.fields['location'].initial = room.location
    form.fields['title'].initial = room.title
    form.fields['capacity'].initial = room.capacity
    form.fields['facilities'].initial = facilities_ids

    return render(request, 'room_booking_app/update_room.html', {'form': form, 'facilities': facilities, 'role': role})


class BookingUpdateView(UpdateView):
    model = Booking
    template_name = 'room_booking_app/rooms_form.html'
    fields = ['title', 'starting_time', 'ending_time']


def clear_session(request):
    request.session.clear()
    return redirect('dashboard')


# ------------------------------------DetailView Views---------------------------
class BookDetailView(DetailView):
    model = Booking


def room_detail_view(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    room = Rooms.objects.get(pk=pk)
    current_time = timezone.localtime()
    suspended_days = Room_Suspension.objects.filter(room=room, start_date__gte=current_time)
    suspension_count = suspended_days.count()

    bookings = Booking.objects.filter(room_id_id=pk).order_by('-date_created')

    facility = room.facilities_ids.split(',')
    facilities = Facility.objects.filter(id__in=facility)

    templatename = 'room_booking_app/room_detail.html'
    context = {"room": room, 'pk': pk, 'bookings': bookings, 'current_time': current_time,
               'facilities': facilities, 'role': role, 'suspended_days': suspended_days,
               'suspension_count': suspension_count}
    return render(request, templatename, context)


# --------------------------------------Book room ---------------------------------
def book_room(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    room = Rooms.objects.get(pk=pk)
    bookings = Booking.objects.filter(room_id_id=pk)
    refreshments = Refreshments.objects.all()
    booked_by = User.objects.get(email=request.user)
    facility = room.facilities_ids.split(',')
    facilities = Facility.objects.filter(id__in=facility)
    approval_settings = Booking_Approval.need_approval

    time_now = timezone.localtime()

    start_of_day = datetime.combine(time_now.date(), time.min)
    end_of_day = datetime.combine(time_now.date(), time.max)

    time_room_booked = Booking.objects.filter(date_start__gte=start_of_day, date_end__lte=end_of_day)

    times_booked = []
    for x in time_room_booked:
        start_hour = x.date_start.hour
        end_hour = x.date_end.hour
        for hour in range(start_hour, end_hour):
            times_booked.append(hour)

    refreshment_ids = []

    if request.method == "POST":
        title = request.POST.get('title')
        starting_time = request.POST.get('starting-date')
        ending_time = request.POST.get('ending-date')
        if starting_time is None:
            messages.error(request, 'Starting time is required.')
            return redirect('book_room', pk)
        # converting datetime to required format
        # book_starting_time = datetime.strptime(starting_time, '%Y-%m-%dT%H:%M')

        # Check if starting_time is greater than current time
        # if book_starting_time < datetime.datetime.now():
        #     messages.error(request, 'Start time must be greater than current time.')
        #     return redirect('book_room', pk)

        # Check if ending_time is greater than starting_time
        elif ending_time < starting_time:
            messages.warning(request, f'ending time cannot be less than starting time')
            return redirect('book_room', pk)

        # Check if the time frame for the booking is not within another approved booking
        overlapping_bookings = Booking.objects.filter(room_id=room,
                                                      date_start__lte=ending_time,
                                                      date_end__gte=starting_time)
        if overlapping_bookings.exists():
            messages.warning(request, f'This room is already booked for this time frame.')
            return redirect('book_room', pk)

        overlapping_suspension = Room_Suspension.objects.filter(room=room,
                                                                start_date__lte=ending_time,
                                                                end_date__gte=starting_time)

        if overlapping_suspension.exists():
            messages.warning(request, f"Meeting Room is unavailable at this time")
            return redirect('book_room', pk)
        status = Booking.STATUS_PENDING  # set default status
        if not approval_settings:
            status = Booking.STATUS_APPROVED

        new_bookings = Booking()
        new_bookings.room_id = room
        new_bookings.user_id = booked_by
        new_bookings.refreshments = ','.join(request.POST.getlist('refreshments'))
        new_bookings.title = title
        new_bookings.status = status
        new_bookings.date_start = starting_time
        new_bookings.date_end = ending_time
        new_bookings.save()

        return redirect('booking_detail', pk=new_bookings.pk)

    templatename = 'room_booking_app/book_room.html'
    context = {"room": room, 'pk': pk, 'bookings': bookings,
               'facilities': facilities, 'role': role, 'times_booked': times_booked, 'refreshments': refreshments}
    return render(request, templatename, context)


def Bookings_View(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    room_booking = Booking.objects.all().order_by('-date_created')
    for book in room_booking:
        time_diff = book.date_end - book.date_start
        book.duration_hours = round(time_diff.total_seconds() / 3600)
    templatename = "room_booking_app/bookings.html"
    context = {'room_booking': room_booking, 'role': role}
    return render(request, templatename, context)


def My_Booking(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    user = User.objects.get(email=request.user)
    upcoming_bookings = Booking.objects.filter(date_start__gte=timezone.localtime())
    bookings = upcoming_bookings.filter(user_id=user).order_by('-date_created')
    for book in bookings:
        time_diff = book.date_end - book.date_start
        book.duration_hours = round(time_diff.total_seconds() / 3600)
    templatename = 'room_booking_app/my_booking.html'
    context = {'bookings': bookings, 'role': role}
    return render(request, templatename, context)


def reset_booking_requirement(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if Booking_Approval.need_approval:
        Booking_Approval.need_approval = False
        messages.success(request, f'bookings will be approved directly upon submission')
        return redirect('settings')
    else:
        Booking_Approval.need_approval = True
        messages.success(request, f'Bookings will require administrator approval')
        return redirect('settings')


def settings_page(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    setting = Booking_Approval.need_approval
    print(setting)
    templatename = 'adminstrator/settings.html'
    context = {'role': role, 'setting': setting}
    return render(request, templatename, context)


def update_my_booking(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    booking = Booking.objects.get(id=pk)
    user = User.objects.get(email=request.user)
    room = Rooms.objects.get(id=booking.room_id_id)
    refreshments = Refreshments.objects.all()

    peripheral = room.facilities_ids.split(',')
    peripherals = Facility.objects.filter(id__in=peripheral)
    form = BookUpdateForm(request.POST, instance=booking)
    if booking.user_id != user:
        messages.error(request, f'No permission to carry out this action')
        return redirect('booking_detail', pk)
    else:

        if form.is_valid():

            title = form.cleaned_data.get('title')
            starting_time = form.cleaned_data.get('starting_time')
            ending_time = form.cleaned_data.get('ending_time')

            # book_starting_time = datetime.datetime.strptime(starting_time, "%Y-%m-%dT%H:%M")

            # Check if starting_time is greater than current time
            if starting_time < timezone.localtime():
                messages.error(request, 'Start time must be greater than current time.')
                return redirect('book_room', pk)

            # Check if ending_time is greater than starting_time
            elif ending_time < starting_time:
                messages.warning(request, f'ending time cannot be less than starting time')
                return redirect('book_room', pk)

            # Check if the time frame for the booking is not within another approved booking
            overlapping_bookings = Booking.objects.filter(room_id=room, status=1,
                                                          date_start__lte=ending_time,
                                                          date_end__gte=starting_time)
            if overlapping_bookings.exists():
                messages.warning(request, f'This room is already booked for this time frame.')
                return redirect('book_room', pk)

            overlapping_suspension = Room_Suspension.objects.filter(room=room,
                                                                    start_date__lte=ending_time,
                                                                    end_date__gte=starting_time)

            if overlapping_suspension.exists():
                messages.warning(request, f"Meeting Room is unavailable at this time")
                return redirect('book_room', pk)

            booking.user_id = user
            booking.title = title
            booking.date_start = starting_time
            booking.date_end = ending_time
            booking.refreshments = ','.join(form.cleaned_data.get('refreshments'))
            booking.save()
            messages.success(request, f'booking updated successfully')
            return redirect('booking_detail', booking.pk)
        else:
            form = BookUpdateForm(instance=booking)

        form.fields['title'].initial = booking.title
        #
        # form.fields['ending_time'].initial = booking.date_end
        # form.fields['refreshments'].initial = booking.refreshments

    templatename = 'room_booking_app/booking_update.html'
    context = {'role': role, 'form': form, 'peripherals': peripherals, 'refreshments': refreshments}
    return render(request, templatename, context)


def booking_detail_view(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    booking = Booking.objects.get(id=pk)
    templatename = 'room_booking_app/booking_detail.html'
    context = {'booking': booking, "role": role}
    return render(request, templatename, context)
