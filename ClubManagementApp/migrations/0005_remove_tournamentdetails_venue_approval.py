# Generated by Django 3.1.4 on 2022-02-20 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ClubManagementApp', '0004_tournamentdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournamentdetails',
            name='venue_approval',
        ),
    ]