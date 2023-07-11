from django.db.models import Model, QuerySet


def create_queryset_from_object(obj: Model) -> QuerySet:
    return obj.__class__.objects.all().filter(pk=obj.pk)
