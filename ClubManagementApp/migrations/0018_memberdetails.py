# Generated by Django 4.0.3 on 2022-04-20 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClubManagementApp', '0017_alter_fixture_team1_alter_fixture_team2'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberDetails',
            fields=[
                ('m_id', models.AutoField(db_column='m_id', primary_key=True, serialize=False)),
                ('m_name', models.CharField(db_column='m_name', max_length=50)),
                ('m_email', models.EmailField(db_column='m_mail', max_length=100)),
                ('m_phno', models.CharField(db_column='m_ph', max_length=10)),
                ('m_passwd', models.CharField(db_column='m_pswd', max_length=120)),
            ],
            options={
                'db_table': 'tb_member',
            },
        ),
    ]
