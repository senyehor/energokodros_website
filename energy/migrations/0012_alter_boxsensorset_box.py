# Generated by Django 4.1.5 on 2023-02-14 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('energy', '0011_alter_boxsensorset_sensor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxsensorset',
            name='box',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='sensor_sets',
                to='energy.box'
                ),
        ),
    ]
