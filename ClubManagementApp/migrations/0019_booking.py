# Generated by Django 4.0.3 on 2022-04-24 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClubManagementApp', '0018_memberdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('tickets', models.IntegerField()),
                ('total', models.FloatField()),
                ('fix_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClubManagementApp.fixture')),
                ('m_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClubManagementApp.memberdetails')),
                ('tournament_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClubManagementApp.tournamentdetails')),
            ],
            options={
                'db_table': 'tb_booking',
            },
        ),
    ]