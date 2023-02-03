from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(User)
admin.site.register(Rooms)
admin.site.register(Campus)
admin.site.register(Booking)
admin.site.register(Facility)
