# Generated by Django 4.0.5 on 2022-06-04 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='accomodation_type',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='adults',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='check_in',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='check_out',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='children',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='n_room_places',
        ),
    ]
