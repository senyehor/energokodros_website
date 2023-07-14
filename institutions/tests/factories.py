import factory
from factory import django


class InstitutionFactory(django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'institution {n}')
    description = factory.Sequence(lambda n: f'institution {n} description')

    class Meta:
        model = 'institutions.Institution'


class AccessLevelFactory(django.DjangoModelFactory):
    code = factory.Sequence(lambda n: n)
    description = factory.Sequence(lambda n: f'level {n} description')

    class Meta:
        model = 'institutions.AccessLevel'


class ObjectFactory(django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'object {n}')
    description = factory.Sequence(lambda n: f'object {n} description')

    class Meta:
        model = 'institutions.Object'
