# Generated by Django 4.1.5 on 2023-02-13 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('energy', '0010_alter_box_box_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxsensorset',
            name='sensor',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name='set', to='energy.sensor'
                ),
        ),
    ]
