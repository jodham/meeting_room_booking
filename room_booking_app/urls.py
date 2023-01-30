from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),

    path('book/room/<int:pk>', book_room, name='book_room'),
    path('bookings/', Bookings_View, name='bookings'),
    path('book/detail/<int:pk>', BookDetailView.as_view(), name='book_detail'),
    path('book/update/<int:pk>', BookingUpdateView.as_view(), name='booking_update'),

    path('room/detail/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('room/create/', CreateRoomView.as_view(), name='create_room'),
    path('room/update/<int:pk>', RoomUpdateView.as_view(), name='room_update'),

    path('session/', clear_session, name='clear_session')
    # path('book/create_book/', BookCreateView.as_view(), name='book_create')
]
