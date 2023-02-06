from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import DetailView, UpdateView

from .forms import RoomForm
from .models import Rooms, Booking, User, Campus, Facility


# Create your views here.
def index(request):
    templatename = 'room_booking_app/index.html'
    context = {}
    return render(request, templatename, context)


@login_required(login_url='signin')
def dashboard(request):
    templatename = 'room_booking_app/rooms.html'
    rooms = Rooms.objects.all()
    context = {'rooms': rooms}
    return render(request, templatename, context)


# ------------------------------room create view------>
from django.shortcuts import render, redirect
from .models import Rooms, Campus, Facility


def create_room_form(request):
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
    context = {'campus': campus, 'facility': facility, 'facilities': facilities}
    return render(request, templatename, context)


# ------------------------------------Update Views---------------------------->
class RoomUpdateView(UpdateView):
    model = Rooms
    form_class = RoomForm
    template_name = 'room_booking_app/update_room.html'
    success_url = 'dashboard'

    def get_object(self, queryset=None):
        room = Rooms.objects.get(id=self.kwargs['pk'])
        return room

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        form.fields['facilities_ids'].initial = ",".join(str(x) for x in self.object.get_facilities_ids())
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            self.object.facilities_ids = ",".join(str(x) for x in form.cleaned_data['facilities_ids'])
            self.object.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})





class BookingUpdateView(UpdateView):
    model = Booking
    template_name = 'room_booking_app/rooms_form.html'
    fields = ['title', 'starting_time', 'ending_time']


def clear_session(request):
    request.session.clear()
    return redirect('dashboard')


# ------------------------------------DetailView Views---------------------------
class RoomDetailView(DetailView):
    model = Rooms


class BookDetailView(DetailView):
    model = Booking


def room_detail_view(request, pk):
    room = Rooms.objects.get(pk=pk)
    bookings = Booking.objects.filter(room_id_id=pk)
    user = request.user
    print(room)
    if request.method == "POST":
        room_id = room
        booked_by = user
        title = request.POST.get('title')
        starting_date = request.POST.get('starting-date')
        ending_date = request.POST.get('ending-date')

        if starting_date < str(timezone.now()):
            messages.error(request, 'choose starting time greater than now')
        elif ending_date <= starting_date:
            messages.error(request, 'choosing ending time beyond starting time')
        else:
            booking = Booking()
            booking.room_id = room_id
            booking.user_id = booked_by
            booking.title = title
            booking.date_start = starting_date
            booking.date_end = ending_date
            booking.save()
    templatename = 'room_booking_app/room_detail.html'
    context = {"room": room, 'bookings': bookings}
    return render(request, templatename, context)


# --------------------------------------Book room ---------------------------------
@login_required(login_url='signin')
def book_room(request, pk):
    room = Rooms.objects.get(id=pk)
    booked_by = User.objects.get(email=request.user)

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
            bookings = Booking()
            bookings.room_id = room
            bookings.booked_by = booked_by
            bookings.title = title
            bookings.starting_time = starting_time
            bookings.ending_time = ending_time
            bookings.save()

            return redirect('bookings')

    templatename = 'room_booking_app/rooms_form.html'
    context = {"room": room, 'pk': pk}
    return render(request, templatename, context)


def Bookings_View(request):
    room_booking = Booking.objects.all()
    templatename = "room_booking_app/bookings.html"
    context = {'room_booking': room_booking}
    return render(request, templatename, context)


def booking_detail_view(request, id):
    booking = Booking.objects.get(id=id)
    templatename = 'room_booking_app/booking_detail.html'
    context = {'booking': booking}
    return render(request, templatename, context)
