# Generated by Django 4.0.5 on 2022-07-26 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('institutions', '0002_rename_object_facilities_alter_facilities_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Facilities',
            new_name='Facility',
        ),
    ]
