from django.urls import path
from.views import *


urlpatterns = [
    path('register', register, name='register'),
    path('', signin, name='signin'),
    path('signout/', signout, name='signout')
]