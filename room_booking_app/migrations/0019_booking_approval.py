# Generated by Django 4.1.2 on 2023-02-23 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0018_facility_category_facility_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking_Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('need_approval', models.BooleanField(default=False)),
            ],
        ),
    ]
