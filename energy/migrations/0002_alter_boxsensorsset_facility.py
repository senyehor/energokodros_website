# Generated by Django 4.1.1 on 2022-10-01 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_rename_facilities_facility'),
        ('energy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxsensorsset',
            name='facility',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.facility'),
        ),
    ]
