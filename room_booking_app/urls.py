
from .views import *
from django.urls import path

# app_name = 'room_booking_app'
urlpatterns = [
    path('index/', index, name='index'),
    path('', dashboard, name='dashboard'),

    path('book/room/<int:pk>', book_room, name='book_room'),
    path('bookings/', Bookings_View, name='bookings'),
    path('booking/mybooking/', My_Booking, name='my_booking'),
    path('book/detail/<int:pk>', booking_detail_view, name='booking_detail'),
    path('booking/update/<int:pk>', my_booking_update, name='my_booking_update'),
    path('book/update/<int:pk>', updateBooking, name='booking_update'),
    path('room/detail/<int:pk>/', room_detail_view, name='room_detail'),
    path('room/create/', create_room_form, name='create_room'),
    path('room/update/<int:pk>', RoomUpdateView, name='room_update'),
    path('room/active_rooms/', activeRooms, name='rooms'),

    path('adminstrator/booking_approval/',  booking_approval_api, name='settings'),
    path('session/', clear_session, name='clear_session'),
    path('update_approval_setting/', update_booking_approval_status, name='update_booking_approval_status'),
    # path('book/create_book/', BookCreateView.as_view(), name='book_create')
]
