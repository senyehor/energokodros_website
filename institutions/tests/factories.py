import factory
from factory import django


class InstitutionFactory(django.DjangoModelFactory):
    institution_name = factory.Sequence(lambda n: f'institution {n}')
    institution_description = factory.Sequence(lambda n: f'institution {n} description')

    class Meta:
        model = 'institutions.Institution'


class AccessLevelFactory(django.DjangoModelFactory):
    level_def = factory.Sequence(lambda n: n)
    level_description = factory.Sequence(lambda n: f'level {n} description')

    class Meta:
        model = 'institutions.AccessLevel'


class ObjectFactory(django.DjangoModelFactory):
    object_name = factory.Sequence(lambda n: f'object {n}')
    object_description = factory.Sequence(lambda n: f'object {n} description')

    class Meta:
        model = 'institutions.Object'
