import factory
from factory import django

from institutions.models import Facility


class FacilityFactory(django.DjangoModelFactory):
    """by default creates root node"""
    name = factory.Sequence(lambda n: f'institution {n}')
    description = factory.Sequence(lambda n: f'institution {n} description')

    @classmethod
    def _create(cls, model_class: 'Facility', *args, **kwargs):
        return model_class.add_root(**kwargs)

    class Meta:
        model = Facility
