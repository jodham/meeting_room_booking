# Generated by Django 4.1.2 on 2023-02-04 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date_actioned',
            field=models.DateTimeField(null=True),
        ),
    ]