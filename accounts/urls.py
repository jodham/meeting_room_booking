from django.urls import path
from.views import *


urlpatterns = [
    path('register', register, name='register'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),

    path('adminstrator/panel/', adminstrator, name='adminstrator_page'),
    path('adminstrator/users', UsersListView, name='system_users'),
    path('adminstrator/users/detail/<int:pk>', user_detail, name='user_detail'),

    path('adminstrator/create/user', add_user, name='create_user'),
    path('adminstrator/user/update/<int:pk>', update_user, name='update_user'),
    path('adminstrator/system_logs/', system_logs, name='system_logs'),
    path('adminstrator/activate/user/<int:id>', activate_deactivate_user, name='activate_deactivate_user'),

    path('adminstrator/peripherals', peripherals, name='peripherals'),
    path('adminstrator/peripheral/create', create_peripheral, name='create_peripheral'),
    path('adminstrator/peripheral/update/<int:pk>', PeripheralUpdateView, name='update_peripheral'),
    path('adminstrator/peripheral/activate_deactivate/<int:pk>', activate_deactivate_peripheral,
         name='activate_deactivate_peripheral'),
    path('adminstrator/rooms/activate_deactivate_room/<int:pk>', activate_deactivate_room,
         name='activate_deactivate_room'),

    path('adminstrator/approve/booking/<int:pk>', approve_booking, name='approve_booking'),
    path('adminstrator/reject/booking/<int:pk>', reject_booking, name='reject_booking'),
    path('user/cancel/booking/<int:pk>', cancel_booking, name='cancel_booking'),
    path('adminstrator/room/suspend/<int:pk>', suspend_room, name='suspend_room')
]
