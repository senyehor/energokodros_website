# Generated by Django 4.1.3 on 2022-12-22 10:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('energy', '0005_rename_box_number_box_box_identifier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxsensorsset',
            name='sensor_number',
            field=models.IntegerField(db_column='sensor_number',
                                      validators=[django.core.validators.MinValueValidator(1),
                                                  django.core.validators.MaxValueValidator(16)]
                                      ),
        ),
        migrations.RenameField(
            model_name='boxsensorsset',
            old_name='sensor_number',
            new_name='sensor_number_in_set',
        ),
    ]