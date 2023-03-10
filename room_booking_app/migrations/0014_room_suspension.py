# Generated by Django 4.1.2 on 2023-02-16 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0013_rooms_suspension_end_rooms_suspension_reason_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room_Suspension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('suspension_reason', models.CharField(blank=True, max_length=250)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_booking_app.rooms')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
