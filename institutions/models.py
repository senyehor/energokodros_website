from django.db import models
from django.utils.translation import gettext as _


class Institution(models.Model):
    institution_id = models.AutoField(
        primary_key=True,
        db_column='institution_id'
    )
    institution_name = models.CharField(
        _('назва закладу'),
        max_length=1000,
        null=False,
        blank=False
    )
    institution_description = models.TextField(
        _('опис закладу'),
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'institutions'
        verbose_name = _('Заклад')
        verbose_name_plural = _('Заклади')

    def __str__(self):
        return self.institution_name


class AccessLevel(models.Model):
    access_level_id = models.AutoField(primary_key=True)
    level_def = models.IntegerField(
        _('код рівню доступу'),
        unique=True,
        null=False,
        blank=False
    )
    level_description = models.TextField(
        _('опис рівню доступу'),
        blank=False,
        null=False
    )

    class Meta:
        db_table = 'access_levels'
        verbose_name = _('Рівень доступу')
        verbose_name_plural = _('Рівні доступу')

    def __str__(self):
        return self.level_description


class Object(models.Model):
    object_id = models.AutoField(primary_key=True)
    object_name = models.CharField(
        _("назва об'єкту"),
        max_length=1000,
        blank=True,
        null=False
    )
    object_description = models.TextField(
        _("опис об'єкту"),
        blank=True,
        null=True
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        null=False,
        related_name='related_objects'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    access_level = models.ForeignKey(
        'AccessLevel',
        models.RESTRICT,
        null=False,
        blank=False,
        related_name='+'
    )

    class Meta:
        db_table = 'objects'
        verbose_name = _("Об'єкт")
        verbose_name_plural = _("Об'єкти")

    def __str__(self):
        return _(f'{self.object_name} в {self.institution}')
