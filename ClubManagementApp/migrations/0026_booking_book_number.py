# Generated by Django 4.0.3 on 2022-04-24 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClubManagementApp', '0025_alter_booking_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='book_number',
            field=models.CharField(default='', max_length=30),
        ),
    ]
