# Generated by Django 5.0.6 on 2024-07-19 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flightapp', '0005_remove_order_flight_order_flights_orderticket_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderticket',
            name='price',
        ),
    ]
