from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from energokodros.settings import MAX_SENSORS_COUNT_PER_BOX, MIN_SENSORS_COUNT_PER_BOX
from institutions.models import Facility


class Box(models.Model):
    box_id = models.AutoField(primary_key=True)
    box_identifier = models.CharField(max_length=256, blank=False, null=False)
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
    box = models.ForeignKey(
        Box,
        models.CASCADE,
        null=False,
        blank=False
    )
    sensor = models.OneToOneField(
        Sensor,
        models.CASCADE,
        null=False,
        related_name='+'
    )
    facility = models.ForeignKey(
        Facility,
        models.CASCADE,
        null=False,
        blank=False,
        related_name='box_sensors_set'
    )
    line_name = models.CharField(
        max_length=1000,
        blank=False,
        null=False
    )
    date_set_in = models.DateTimeField(
        auto_now_add=True,
        null=False
    )
    sensor_number = models.IntegerField(
        null=False,
        blank=False,
        validators=(
            MinValueValidator(MIN_SENSORS_COUNT_PER_BOX),
            MaxValueValidator(MAX_SENSORS_COUNT_PER_BOX)
        )
    )

    class Meta:
        db_table = 'boxes_sets'
