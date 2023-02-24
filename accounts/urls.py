from django.urls import path

from room_booking_app.views import settings_page, reset_booking_requirement
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
    path('adminstrator/peripheral/update/<int:pk>', PeripheralUpdateView.as_view(), name='update_peripheral'),
    path('adminstrator/peripheral/activate_deactivate/<int:pk>', activate_deactivate_peripheral,
         name='activate_deactivate_peripheral'),
    path('adminstrator/rooms/activate_deactivate_room/<int:pk>', activate_deactivate_room,
         name='activate_deactivate_room'),

    path('adminstrator/approve/booking/<int:pk>', approve_booking, name='approve_booking'),
    path('adminstrator/reject/booking/<int:pk>', reject_booking, name='reject_booking'),
    path('user/cancel/booking/<int:pk>', cancel_booking, name='cancel_booking'),
    path('adminstrator/room/suspend/<int:pk>', suspend_room, name='suspend_room'),

    path('administrator/facility/categories', facility_category, name='facility_category'),
    path('administrator/categories/create', add_facility_category, name='add_category'),
    path('administrator/categories/edit/<int:pk>', edit_facility_category, name='edit_facility_category'),

    path('administrator/campus/create', add_campus, name='add_campus'),
    path('administrator/campus/<int:pk>', CampusUpdateView.as_view(), name='edit_campus'),
    path('administrator/campus/list', Campuses, name='campus_list'),

    path('administrator/settings', settings_page, name='settings'),
    path('administrator/set', reset_booking_requirement, name='reset'),

    path('administrator/refreshments/list', Refreshments_View, name='refreshments_list'),
    path('administrator/refreshments/create', Add_refreshment, name='add_refreshment'),
    path('administrator/refreshments/<int:pk>/edit', edit_refreshment, name='edit_refreshment'),


]
