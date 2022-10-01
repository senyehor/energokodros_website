from django.db import models

from institutions.models import Facility


class Box(models.Model):
    box_id = models.AutoField(primary_key=True)
    box_number = models.CharField(max_length=256, blank=False, null=False)
    box_description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'boxes'


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_number = models.IntegerField(blank=False, null=False)
    sensor_description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'sensors'


class BoxSensorsSet(models.Model):
    boxes_set_id = models.AutoField(primary_key=True)
    box = models.ForeignKey(Box, models.CASCADE, null=False)
    sensor = models.OneToOneField(Sensor, models.RESTRICT, null=False)
    facility = models.ForeignKey(Facility, models.CASCADE, blank=True, null=True)
    line_name = models.CharField(max_length=1000, blank=False, null=False)
    date_set_in = models.DateTimeField(blank=True, null=True)
    sensor_number = models.IntegerField()

    class Meta:
        db_table = 'boxes_sets'
