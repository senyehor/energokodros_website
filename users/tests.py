import random

import factory
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from factory import django

User = get_user_model()


class UserTest(TestCase):
    def setUp(self):
        self.valid_email = 'valid@email.com'
        self.some_password = 'some_password'
        self.valid_full_name = "Тестове Валідне Ім'я"

    def test_creating_user(self):
        email = self.valid_email
        raw_password = self.some_password
        name = self.valid_full_name
        user = User.objects.create(email=email, password=raw_password, full_name=name)
        self.assertEqual(email, user.email, _('user email was set incorrectly'))
        self.assertTrue(user.check_password(raw_password), _('user password was set incorrectly'))
        self.assertEqual(name, user.full_name, _('user full name was set incorrectly'))
        self.assertEqual(email, user.get_username(), _('email is not used as username'))

    def test_creating_with_incorrect_fields_sets(self):
        with self.assertRaises(TypeError, msg=_('User was created with wrong fields set')):
            User.objects.create()
        with self.assertRaises(TypeError, msg=_('User was created with wrong fields set')):
            User.objects.create(full_name=self.valid_full_name)
        with self.assertRaises(TypeError, msg=_('User was created with wrong fields set')):
            User.objects.create(email=self.valid_email)
        with self.assertRaises(TypeError, msg=_('User was created with wrong fields set')):
            User.objects.create(full_name=self.valid_full_name, email=self.valid_email)

    def test_full_name_check(self):
        def test_for_names_list(names: list[str], should_throw: bool):
            for name in names:
                try:
                    user = User.objects.create(
                        full_name=name,
                        email=self.valid_email,
                        password=self.some_password
                    )
                    user.delete()
                except ValidationError:
                    if not should_throw:
                        assert False, _('validating full name throws exception for a valid name')

        correct_names_list = [
            """П'ятницький Хотибор Денисович""",
            """Никоненко Лаврентій-Арсен Полянович""",
            """Слюсар Наслав Денисович""",
        ]
        incorrect_names_list = [
            'Некоректне',
            "Некоректне Ім'я",
            'Incorrect Name Example',
            'Некорректный Пример Имени',
        ]
        test_for_names_list(correct_names_list, should_throw=False)
        test_for_names_list(incorrect_names_list, should_throw=True)

    def test_creating_admin(self):
        admin = User.objects.create(
            full_name=self.valid_full_name,
            email=self.valid_email,
            password=self.some_password,
            is_admin=True
        )
        self.assertTrue(admin.is_admin)


class UserFactory(django.DjangoModelFactory):
    password = factory.Sequence(lambda n: f'generated_password{n}')
    email = factory.Sequence(lambda n: f'generated_email{n}@email.com')
    full_name = factory.Sequence(lambda: UserFactory.full_name)

    @staticmethod
    def generate_full_name():
        first_names = [
            'Яснолик-Гузь',
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
            "В'ячеславович"
        ]
        return " ".join([
            random.choice(first_names),
            random.choice(second_names),
            random.choice(patronims)
        ])

    class Meta:
        model = User
