from django.db import models
from django.utils.translation import gettext as _


class Institution(models.Model):
    institution_id = models.AutoField(primary_key=True)
    name = models.CharField(
        _('назва закладу'),
        max_length=1000,
        null=False,
        blank=False,
        db_column='institution_name'
    )
    description = models.TextField(
        _('опис закладу'),
        null=False,
        blank=False,
        db_column='institution_description'
    )

    class Meta:
        db_table = 'institutions'
        verbose_name = _('Заклад')
        verbose_name_plural = _('Заклади')

    def __str__(self):
        return self.name


class AccessLevel(models.Model):
    access_level_id = models.AutoField(primary_key=True)
    code = models.IntegerField(
        _('код рівню доступу'),
        unique=True,
        null=False,
        blank=False,
        db_column='level_def'
    )
    description = models.TextField(
        _('опис рівню доступу'),
        blank=False,
        null=False,
        db_column='level_description'
    )

    class Meta:
        db_table = 'access_levels'
        verbose_name = _('Рівень доступу')
        verbose_name_plural = _('Рівні доступу')

    def __str__(self):
        return self.description


class Object(models.Model):
    object_id = models.AutoField(primary_key=True)
    name = models.CharField(
        _("назва об'єкту"),
        max_length=1000,
        blank=True,
        null=False,
        db_column='object_name'
    )
    description = models.TextField(
        _("опис об'єкту"),
        blank=True,
        null=True,
        db_column='object_description'
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
        AccessLevel,
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
        return _(f'{self.name} в {self.institution}')
