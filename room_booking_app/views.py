from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import BookingForm
from .models import Room, Bookings


# Create your views here.
def index(request):
    templatename = 'room_booking_app/index.html'
    context = {}
    return render(request, templatename, context)


@login_required(login_url='signin')
def dashboard(request):
    templatename = 'room_booking_app/dashboard.html'
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, templatename, context)


# ------------------------------room create view------>
class CreateRoomView(CreateView):
    model = Room
    fields = ['room_number', 'campus_name', 'room_name', 'room_location', 'room_capacity']

    def form_valid(self, form):
        return super().form_valid(form)


# ------------------------------------Room update---------------------------->
class RoomUpdateView(UpdateView):
    model = Room
    fields = ['room_number', 'campus_name', 'room_name', 'room_location', 'room_capacity']

    def form_valid(self, form):
        return super().form_valid(form)


# ------------------------------------DetailView---------------------------
class RoomDetailView(DetailView):
    model = Room


class BookDetailView(DetailView):
    model = Bookings


@login_required(login_url='signin')
def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        room_number = request.POST.get('room_number')
        bookedby = request.POST.get('bookedby')
        title = request.POST.get('meeting_title')
        starting_date = request.POST.get('starting_date')
        starting_time = request.POST.get('starting_time')
        ending_date = request.POST.get('ending_date')
        ending_time = request.POST.get('ending_time')

        bookings = Bookings()
        bookings.room_id = room_number
        bookings.booked_by = bookedby
        bookings.title = title
        bookings.starting_date = starting_date
        bookings.starting_time = starting_time
        bookings.ending_date = ending_date
        bookings.ending_time = ending_time
        bookings.save()
        return redirect('bookings')

    templatename = 'room_booking_app/book_room_form.html'
    context = {"room": room}
    return render(request, templatename, context)


def Bookings_View(request):
    room_booking = Bookings.objects.all()
    templatename = "room_booking_app/bookings.html"
    context = {'room_booking': room_booking}
    return render(request, templatename, context)
