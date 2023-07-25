import functools
from typing import Callable, NamedTuple

from django.db import models
from django.utils.translation import gettext as _
from treebeard.ns_tree import NS_Node, NS_NodeManager


class FacilityManager(NS_NodeManager):
    def institutions(self):
        # we separate a regular facility (that have a parent facility)
        # and institution, that are on top of hierarchy
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

    class MoveOptions(NamedTuple):
        # library gives a lot of options, but that much is not needed
        # by default last-sibling is used so last-child was chosen
        CHILD = 'last-child'
        SIBLING = 'last-sibling'

    def move(self, target: 'Facility', pos: MoveOptions):  # noqa pylint: disable=W0222
        super().move(target, pos)

    def get_institution(self) -> 'Facility':
        return self.get_root()

    class Meta:
        db_table = 'facilities'
        verbose_name = _("Об'єкт")
        verbose_name_plural = _("Об'єкти")

    def __str__(self):
        return _(f'{self.name}')

    def enable_db_auto_refresh_for_add_or_move(self):
        if hasattr(self, '__db_auto_refresh_enabled'):
            if self.__db_auto_refresh_enabled: # pylint: disable=E0203
                return

        def refresh_from_db_wrapper(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                self.refresh_from_db()
                return res

            return wrapper

        methods_to_wrap = (self.add_root, self.add_child, self.add_sibling, self.move)
        for method in methods_to_wrap:
            setattr(self, method.__name__, refresh_from_db_wrapper(method))
        self.__db_auto_refresh_enabled = True

    # methods below are not implemented for nested set in django_treebeard, so
    # currently they are just 'stubbed'
    @classmethod
    def find_problems(cls):
        raise NotImplementedError

    @classmethod
    def fix_tree(cls):
        raise NotImplementedError
