from django.contrib import admin

from .models import*

# Register your models here.
admin.site.register(User)
admin.site.register(Rooms)
admin.site.register(Campus)
admin.site.register(Booking)
admin.site.register(Facility)
admin.site.register(Roles)
admin.site.register(Room_Suspension)
admin.site.register(Refreshments)
admin.site.register(Booking_Approval)
admin.site.register(System_Logs)
