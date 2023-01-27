from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import BookingForm
from .models import *


# Create your views here.
def index(request):
    templatename = 'room_booking_app/index.html'
    context = {}
    return render(request, templatename, context)


def dashboard(request):
    templatename = 'room_booking_app/dashboard.html'
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, templatename, context)


def roomDetail(request, id):
    templatename = 'room_booking_app/room_detail.html'
    room = Room.objects.get(room_number=id)
    bookings = Bookings.objects.filter(Q(room_id=id))
    context = {'room': room, 'bookings': bookings}
    return render(request, templatename, context)


def book_room(request, id):
    room_number = Room.objects.get(room_id=id)
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user, room_id=room_number)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BookingForm()
    templatename = 'room_booking_app/book_room_form.html'
    context = {"room_number": room_number, 'form': form}
    return render(request, templatename, context)
