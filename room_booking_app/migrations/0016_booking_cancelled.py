# Generated by Django 4.1.2 on 2023-02-16 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0015_remove_rooms_is_suspended_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]