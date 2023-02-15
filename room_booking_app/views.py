# from django.shortcuts import render, redirect
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView

from .controllers import *
from .forms import RoomForm
from .models import Booking, User
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
    rooms = Rooms.objects.all().order_by('-date_created')
    context = {'rooms': rooms, 'role': role}
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
    bookings = Booking.objects.filter(room_id_id=pk)
    facility = room.facilities_ids.split(',')
    facilities = Facility.objects.filter(id__in=facility)

    templatename = 'room_booking_app/room_detail.html'
    context = {"room": room, 'pk': pk, 'bookings': bookings, 'facilities': facilities, 'role': role}
    return render(request, templatename, context)


# --------------------------------------Book room ---------------------------------
def book_room(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    room = Rooms.objects.get(pk=pk)
    bookings = Booking.objects.filter(room_id_id=pk)
    booked_by = User.objects.get(email=request.user)
    facility = room.facilities_ids.split(',')
    facilities = Facility.objects.filter(id__in=facility)
    if request.method == "POST":
        title = request.POST.get('title')
        starting_time = request.POST.get('starting-date')
        ending_time = request.POST.get('ending-date')
        if starting_time is None:
            messages.error(request, 'Starting time is required.')
            return redirect('book_room', pk)
        # converting datetime to required format
        book_starting_time = datetime.datetime.strptime(starting_time, "%Y-%m-%dT%H:%M")

        # Check if starting_time is greater than current time
        if book_starting_time < datetime.datetime.now():
            messages.error(request, 'Start time must be greater than current time.')
            return redirect('book_room', pk)

        # Check if ending_time is greater than starting_time
        elif ending_time < starting_time:
            messages.warning(request, 'ending time cannot be less than starting time')
            return redirect('book_room', pk)

        # Check if the time frame for the booking is not within another approved booking
        overlapping_bookings = Booking.objects.filter(room_id=room, status=1,
                                                      date_start__lte=ending_time,
                                                      date_end__gte=starting_time)
        if overlapping_bookings.exists():
            messages.warning(request, 'This room is already booked for this time frame.')
            return redirect('book_room', pk)

        bookings = Booking()
        bookings.room_id = room
        bookings.user_id = booked_by
        bookings.title = title
        bookings.date_start = starting_time
        bookings.date_end = ending_time
        bookings.save()

        return redirect('bookings')

    templatename = 'room_booking_app/book_room.html'
    context = {"room": room, 'pk': pk, 'bookings': bookings, 'facilities': facilities, 'role': role}
    return render(request, templatename, context)


def Bookings_View(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    room_booking = Booking.objects.all().order_by('-date_created')
    templatename = "room_booking_app/bookings.html"
    context = {'room_booking': room_booking, 'role': role}
    return render(request, templatename, context)


def booking_detail_view(request, pk):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None
    booking = Booking.objects.get(id=pk)
    # booking = book.filter(Q(date_end > ))
    templatename = 'room_booking_app/booking_detail.html'
    context = {'booking': booking, "role": role}
    return render(request, templatename, context)
