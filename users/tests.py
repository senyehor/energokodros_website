import random
from typing import TypedDict

import factory
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse_lazy
from factory import django

from institutions.tests import InstitutionFactory
from users.models import UserRegistrationData, UserRegistrationRequest

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
        self.assertEqual(email, user.email, 'user email was set incorrectly')
        self.assertTrue(user.check_password(raw_password), 'user password was set incorrectly')
        self.assertEqual(name, user.full_name, 'user full name was set incorrectly')
        self.assertEqual(email, user.get_username(), 'email is not used as username')

    def test_creating_with_incorrect_fields_sets(self):
        with self.assertRaises(TypeError, msg='User was created with wrong fields set'):
            User.objects.create()
        with self.assertRaises(TypeError, msg='User was created with wrong fields set'):
            User.objects.create(full_name=self.valid_full_name)
        with self.assertRaises(TypeError, msg='User was created with wrong fields set'):
            User.objects.create(email=self.valid_email)
        with self.assertRaises(TypeError, msg='User was created with wrong fields set'):
            User.objects.create(full_name=self.valid_full_name, email=self.valid_email)

    def test_full_name_check(self):
        def test_for_names_list(names: list[str], should_throw: bool):
            for name in names:
                try:
                    User.objects.create(
                        full_name=name,
                        email=self.valid_email,
                        password=self.some_password
                    )
                except ValidationError:
                    if not should_throw:
                        assert False, 'validating full name throws exception for a valid name'

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


class UserRegistrationDataFactory(UserFactory):
    email_code = factory.Sequence(lambda n: f'code {n}')

    class Meta:
        model = UserRegistrationData


class UserRegistrationRequestFormsetTest(TestCase):
    # new users will not be created alone, only with application for institution
    # + position, or we will have applications for
    # new roles (user, institution, access_level) from existing users
    def setUp(self):
        self.client = Client()
        self.raw_password = '%tv{,,E)36'
        self.message = 'певне повідомлення'
        # using .build() to not save user
        self.user: User = UserFactory.build(password=self.raw_password)
        self.institution = InstitutionFactory()

    def test_with_correct_data_set(self):
        # HUGE WARNING: when debugging something VERY strange is
        # happening, (if I have a breakpoint outside of test)
        # UserRegistrationRequestForm will fail validation with no apparent reason
        # django request ticket # todo
        data = self.__get_form_data()
        data['full_name'] = self.user.full_name
        data['email'] = self.user.email
        data['password1'] = self.raw_password
        data['password2'] = self.raw_password
        data['registration_requests-0-institution'] = str(self.institution.pk)
        resp: HttpResponse = self.client.post(
            reverse_lazy('register'),
            {
                **data
            },
            follow=True
        )
        self.assertEqual(
            resp.status_code,
            200,
            'form validation failed with correct data'
        )
        try:
            user = User.objects.get(
                full_name=self.user.full_name,
                email=self.user.email
            )
        except ObjectDoesNotExist:
            assert False, 'user is not created'
        except MultipleObjectsReturned:
            assert False, 'multiple users are created'
        try:
            user_registration_request = UserRegistrationRequest.objects.get(
                user=user
            )
        except ObjectDoesNotExist:
            assert False, 'user registration request is not created'
        except MultipleObjectsReturned:
            assert False, 'multiple user registration requests are created'
        self.assertEqual(
            user_registration_request.institution.pk,
            self.institution.pk,
            'incorrect institution is saved for registration request'
        )
