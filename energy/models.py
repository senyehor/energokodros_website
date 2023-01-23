from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from energokodros.settings import SENSOR_COUNT_PER_BOX
from institutions.models import Facility


class Box(models.Model):
    box_id = models.AutoField(primary_key=True)
    box_identifier = models.CharField(max_length=256, blank=False, null=False)
    box_description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'boxes'

    def __str__(self):
        return _(f'Ящик {self.box_identifier}')

    def get_absolute_url(self):
        return reverse_lazy('edit-box', kwargs={'pk': self.pk})


class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_number = models.IntegerField(blank=False, null=False)
    sensor_description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'sensors'

    def __str__(self):
        return _(f'Сенсор {self.sensor_number}')

    def get_absolute_url(self):
        return reverse_lazy('edit-sensor', kwargs={'pk': self.pk})


class BoxSensorsSet(models.Model):
    _SENSOR_STARTING_NUMBER = 1
    boxes_set_id = models.AutoField(primary_key=True)
    box = models.ForeignKey(
        Box,
        models.CASCADE,
        null=False,
        blank=False,
        related_name='box_sensor_sets'
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
    sensor_number_in_set = models.IntegerField(
        null=False,
        blank=False,
        validators=(
            MinValueValidator(_SENSOR_STARTING_NUMBER),
            MaxValueValidator(SENSOR_COUNT_PER_BOX)
        ),
        db_column='sensor_number'
    )

    class Meta:
        db_table = 'boxes_sets'

    def __str__(self):
        return _(f'{self.sensor} із {self.box}')
