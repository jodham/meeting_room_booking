# Generated by Django 4.1.2 on 2023-03-12 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0020_booking_extra_peripherals_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='facilities_ids',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]