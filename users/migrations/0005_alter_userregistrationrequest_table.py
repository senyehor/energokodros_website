# Generated by Django 4.0.4 on 2022-06-21 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userrole_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userregistrationrequest',
            table='users_registration_requests',
        ),
    ]
