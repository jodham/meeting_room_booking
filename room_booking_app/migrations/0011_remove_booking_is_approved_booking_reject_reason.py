# Generated by Django 4.1.2 on 2023-02-15 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0010_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='booking',
            name='reject_reason',
            field=models.TextField(null=True),
        ),
    ]