# Generated by Django 4.1.1 on 2022-10-01 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0003_rename_facilities_facility'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('box_id', models.AutoField(primary_key=True, serialize=False)),
                ('box_number', models.CharField(max_length=256)),
                ('box_description', models.TextField()),
            ],
            options={
                'db_table': 'boxes',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(primary_key=True, serialize=False)),
                ('sensor_number', models.IntegerField()),
                ('sensor_description', models.TextField()),
            ],
            options={
                'db_table': 'sensors',
            },
        ),
        migrations.CreateModel(
            name='BoxSensorsSet',
            fields=[
                ('boxes_set_id', models.AutoField(primary_key=True, serialize=False)),
                ('line_name', models.CharField(max_length=1000)),
                ('date_set_in', models.DateTimeField(blank=True, null=True)),
                ('sensor_number', models.IntegerField()),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='energy.box')),
                ('facility', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='institutions.facility')),
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='energy.sensor')),
            ],
            options={
                'db_table': 'boxes_sets',
            },
        ),
    ]