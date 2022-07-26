import random

import factory
from django.contrib.auth import get_user_model
from factory import django

from institutions.tests.factories import FacilityFactory
from users.models import UserRoleApplication

User = get_user_model()


class UserFactory(django.DjangoModelFactory):
    password = factory.Sequence(lambda n: f'generated_password{n}')
    email = factory.Sequence(lambda n: f'generated_email{n}@email.com')

    @factory.lazy_attribute
    def full_name(self):
        first_names = [
            'Яснолик-Гузь',
            'Шарль',
            'Златоус',
            'Милована',
        ]
        second_names = [
            'Оробко',
            'Білоножко',
            'Даценко',
            'Гасенко',
        ]
        patronims = [
            'Адріанович',
            'Романович',
            'Мстиславович',
            "В'ячеславович"
        ]
        return " ".join([
            random.choice(first_names),
            random.choice(second_names),
            random.choice(patronims)
        ])

    class Meta:
        model = User


class UserRoleApplicationFactory(django.DjangoModelFactory):
    class Meta:
        model = UserRoleApplication

    user = factory.SubFactory(UserFactory, is_active=True)
    institution = factory.SubFactory(FacilityFactory)
    message = factory.Faker('text', max_nb_chars=50)
