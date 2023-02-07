from django.urls import path
from.views import *


urlpatterns = [
    path('register', register, name='register'),
    path('', signin, name='signin'),
    path('signout/', signout, name='signout'),

    path('adminstrator/panel/', adminstrator, name='adminstrator_page'),
    path('adminstrator/users', UsersListView.as_view(), name='system_users')
]