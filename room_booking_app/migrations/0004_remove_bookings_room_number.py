# Generated by Django 4.1.5 on 2023-01-29 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0003_room_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='room_number',
        ),
    ]
