from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import BookingForm
from .models import Room, Bookings, MyUser, Resource


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


# ------------------------------------Update Views---------------------------->
class RoomUpdateView(UpdateView):
    model = Room
    fields = ['room_number', 'campus_name', 'room_name', 'room_location', 'room_capacity']

    def form_valid(self, form):
        return super().form_valid(form)


class BookingUpdateView(UpdateView):
    model = Bookings
    template_name = 'room_booking_app/book_room_form.html'
    fields = ['title', 'starting_time', 'ending_time']


def clear_session(request):
    request.session.clear()
    return redirect('dashboard')


# ------------------------------------DetailView Views---------------------------
class RoomDetailView(DetailView):
    model = Room


class BookDetailView(DetailView):
    model = Bookings


def room_detail_view(request, pk):
    room = Room.objects.get(pk=pk)
    resources = Resource.objects.filter(rm_id_id=pk)
    bookings = Bookings.objects.filter(room_id_id=pk)
    paginator = Paginator(bookings, 2)
    page = request.GET.get('page')
    bookings = paginator.get_page(page)
    templatename = 'room_booking_app/room_detail.html'
    context = {"room": room, 'resources': resources, 'bookings': bookings}
    return render(request, templatename, context)


# --------------------------------------Book room ---------------------------------
@login_required(login_url='signin')
def book_room(request, pk):
    room = Room.objects.get(room_number=pk)
    booked_by = MyUser.objects.get(email=request.user)

    if request.method == "POST":
        title = request.POST.get('meeting_title')
        starting_time = request.POST.get('starting_time')
        ending_time = request.POST.get('ending_time')

        if starting_time < str(timezone.now()):
            messages.error(request, 'Start time must be greater than current time.')
            # return redirect('room_booking_app:book_room', room)
        elif ending_time < starting_time:
            messages.warning(request, 'ending time cannot be less than starting time')

        else:
            bookings = Bookings()
            bookings.room_id = room
            bookings.booked_by = booked_by
            bookings.title = title
            bookings.starting_time = starting_time
            bookings.ending_time = ending_time
            bookings.save()

            # subject = 'Room Booking Notification'
            # message = 'Your room has been booked successfully.'
            # from_email = 'jodham.wanjala@zetech.ac.ke'
            # to_list = ['sikutwajotham@gmail.com']
            # send_mail(subject, message, from_email, to_list, fail_silently=False)

            return redirect('bookings')

    templatename = 'room_booking_app/book_room_form.html'
    context = {"room": room, 'pk': pk}
    return render(request, templatename, context)


def Bookings_View(request):
    room_booking = Bookings.objects.all()
    templatename = "room_booking_app/bookings.html"
    context = {'room_booking': room_booking}
    return render(request, templatename, context)
