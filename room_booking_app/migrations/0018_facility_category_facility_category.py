# Generated by Django 4.1.2 on 2023-02-22 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0017_refreshments_booking_refreshments_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='facility',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='room_booking_app.facility_category'),
            preserve_default=False,
        ),
    ]
