# Generated by Django 4.1.2 on 2023-02-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0004_remove_rooms_facilities_ids_rooms_facilities_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='facilities_ids',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
