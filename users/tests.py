import random

import factory
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from factory import django


class UserTest(TestCase):
    def test_creating_user(self):
        email = 'correct@email.com'
        raw_password = 'correct_password'
        name = 'Ковалів Яр Володимирович'
        user = UserFactory(email=email, password=raw_password, full_name=name)
        self.assertEqual(email, user.email, _("user email was set incorrectly"))
        self.assertTrue(user.check_password(raw_password), _("user password was set incorrectly"))
        self.assertEqual(name, user.full_name, _("user full name was set incorrectly"))
        self.assertEqual(name, user.get_username(), _("email is not used as username"))

    def test_creating_with_incorrect_fields(self):
        with self.assertRaises(TypeError):
            UserFactory.create()
    def test_full_name_validation(self):  # noqa pylint: disable=no-self-use
        names_list = [
            """П'ятницький Хотибор Денисович""",
            """Никоненко Лаврентій-Арсен Полянович""",
            """Слюсар Наслав Денисович""",
        ]
        for name in names_list:
            try:
                UserFactory(full_name=name)
            except ValidationError:
                assert False, _('validating full name throws exception for a valid name')


class UserFactory(django.DjangoModelFactory):
    password = factory.Sequence(lambda n: f'generated_password{n}')
    email = factory.Sequence(lambda n: f'generated_email{n}@email.com')

    def full_name(self):  # noqa: E pylint: disable=no-self-use
        first_names = [
            'Яснолик',
            'Шарль',
            'Златоус'
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
            'Борисівна'
        ]
        return " ".join([random.choice(first_names),
                         random.choice(second_names),
                         random.choice(patronims)]
                        )

    class Meta:
        model = get_user_model()
