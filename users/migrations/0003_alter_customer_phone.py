# Generated by Django 4.0.5 on 2022-06-04 04:09

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customer_accomodation_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
    ]
