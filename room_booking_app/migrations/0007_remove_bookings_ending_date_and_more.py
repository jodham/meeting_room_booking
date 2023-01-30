# Generated by Django 4.1.5 on 2023-01-30 09:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0006_bookings_ending_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookings',
            name='ending_date',
        ),
        migrations.RemoveField(
            model_name='bookings',
            name='starting_date',
        ),
        migrations.AlterField(
            model_name='bookings',
            name='ending_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='starting_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
