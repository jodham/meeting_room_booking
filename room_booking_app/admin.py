from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Room)
admin.site.register(Resource)
admin.site.register(Campus_branch)
admin.site.register(ResourceUtilization)
admin.site.register(Bookings)
admin.site.register(UserActivity)