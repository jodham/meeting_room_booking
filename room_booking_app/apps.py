from django.apps import AppConfig


class RoomBookingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'room_booking_app'

    def ready(self):
        import room_booking_app.controllers