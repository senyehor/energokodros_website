from django.db import models
from django.db.models import QuerySet


def object_to_queryset(obj: models.Model) -> QuerySet:
    return type(obj).objects.filter(pk=obj.pk)