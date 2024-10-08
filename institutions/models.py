from django.db import models
from django.db.transaction import atomic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from treebeard.ns_tree import NS_Node, NS_NodeManager

from energy.models import Box, BoxSensorSet, Sensor


class FacilityManager(NS_NodeManager):
    def get_institutions(self):
        # we separate a regular facility (that have a parent facility)
        # and institutions, that are on top of hierarchy
        return self.model.get_root_nodes()


class Facility(NS_Node):
    name = models.CharField(
        _("назва об'єкту"),
        max_length=1000,
        blank=True,
        null=False,
        db_column='name'
    )
    description = models.TextField(
        _("опис об'єкту"),
        blank=True,
        null=True,
        db_column='description'
    )

    objects = FacilityManager()

    @method_decorator(atomic)
    def delete(self, *args, **kwargs):
        facility_with_all_descendants = self.get_tree(self)
        box_sensor_sets_for_facility_with_all_descendants = BoxSensorSet.objects.filter(
            facility__in=facility_with_all_descendants
        ).all()
        boxes = Box.objects.filter(
            sensor_sets__in=box_sensor_sets_for_facility_with_all_descendants
        )
        sensors = Sensor.objects.filter(
            set__in=box_sensor_sets_for_facility_with_all_descendants
        ).only('sensor_id')
        # trick to force evaluation of qs, as box_sensor_sets are going to be deleted,
        # and qs will be empty in such case
        sensors = list(sensors)
        deleted_boxes_data = boxes.delete()
        deleted_sensors_data = Sensor.objects.filter(
            pk__in=[sensor.pk for sensor in sensors]
        ).delete()
        super_deletion_results = super().delete(*args, **kwargs)
        return super_deletion_results, deleted_boxes_data, deleted_sensors_data

    class Meta:
        db_table = 'facilities'
        verbose_name = _("Об'єкт")
        verbose_name_plural = _("Об'єкти")

    def __str__(self):
        if self.is_root():
            return _(f'заклад {self.name}')
        return _(f"об'єкт {self.name} із {self.get_institution().name}")

    def get_absolute_url(self):
        return reverse_lazy('edit-facility', kwargs={'pk': self.pk})

    def get_institution(self) -> 'Facility':
        return self.get_root()

    def is_institution(self) -> bool:
        return self.is_root()

    # methods below are not implemented for nested set in django_treebeard, so
    # currently they are just 'stubbed'
    @classmethod
    def find_problems(cls):
        raise NotImplementedError

    @classmethod
    def fix_tree(cls):
        raise NotImplementedError
