from django.db import models


class Institution(models.Model):
    institution_id = models.AutoField(
        primary_key=True,
        db_column='institution_id'
    )
    institution_name = models.CharField(
        max_length=1000,
        null=False,
        blank=False
    )
    institution_description = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'institutions'


class AccessLevel(models.Model):
    access_level_id = models.AutoField(primary_key=True)
    level_def = models.IntegerField(unique=True, null=False, blank=False)
    level_description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'access_levels'


class Object(models.Model):
    object_id = models.AutoField(primary_key=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    object_name = models.CharField(max_length=1000, blank=True, null=False)
    object_description = models.TextField(blank=True, null=True)
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
