from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from treebeard.ns_tree import NS_Node, NS_NodeManager


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

    # methods below are not implemented for nested set in django_treebeard, so
    # currently they are just 'stubbed'
    @classmethod
    def find_problems(cls):
        raise NotImplementedError

    @classmethod
    def fix_tree(cls):
        raise NotImplementedError
