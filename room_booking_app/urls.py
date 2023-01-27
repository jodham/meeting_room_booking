from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('room/detail/<int:id>', roomDetail, name='room_detail'),
    path('book/room/<int:id', book_room, name='book_room')
]