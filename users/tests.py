import random
from typing import TypedDict

import factory
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse, reverse_lazy
from factory import django

from institutions.models import Institution
from institutions.tests import InstitutionFactory
from users.logic import EmailConfirmationController
from users.models import UserRoleApplication
from utils.crypto import hide_int

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


_user_registration_data_dict = TypedDict(
    'data_dict',  # noqa
    {
        'full_name':                           str,
        'email':                               str,
        'password1':                           str,
        'password2':                           str,
        # part below is related to UserRegistrationRequestForm and keys are generated
        # automatically by UserRegistrationRequestFormset and for some reason always
        # include empty id and user, even though they are not included in
        # UserRegistrationRequestForm, so it`s keys are just copied
        # from knowingly correct form
        'registration_requests-0-institution': str,
        'registration_requests-0-message':     str,

        'registration_requests-0-id':          str,
        'registration_requests-0-user':        str,

        'registration_requests-TOTAL_FORMS':   str,
        'registration_requests-INITIAL_FORMS': str,
        'registration_requests-MIN_NUM_FORMS': str,
        'registration_requests-MAX_NUM_FORMS': str,
    }
)


class UserRegistrationTest(TestCase):
    # here new users creating along with application for institution
    # + position is tested
    def setUp(self):
        self.client = Client()
        self.raw_password = '%tv{,,E)36'
        self.message = 'some message'
        self.user: User = UserFactory.build(password=self.raw_password)
        self.institution = InstitutionFactory()

    def test_with_correct_data_set(self):
        resp = self._send_correct_registration_data()
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
        try:
            UserRoleApplication.objects.get(
                user=user
            )
        except ObjectDoesNotExist:
            assert False, 'user registration request is not created'
        except MultipleObjectsReturned:
            assert False, 'multiple user registration requests are created'

    def test_user_and_role_application_is_created_correctly(self):
        self._send_correct_registration_data()
        user = User.objects.get(
            full_name=self.user.full_name,
            email=self.user.email
        )
        self.assertFalse(
            user.is_active,
            'user must me inactive on registration (email unconfirmed)'
        )
        user_registration_request = UserRoleApplication.objects.get(
            user=user
        )
        self.assertEqual(
            user_registration_request.application__institution,
            self.institution,
            'registration request is set for wrong institution'
        )

    def test_email_confirmation(self):
        self._send_correct_registration_data()
        # here we mock request just to use it`s is_secure and get_host to generate link
        request = RequestFactory().get('')
        _ = EmailConfirmationController
        # here we get just first user, as it should be created and be the only one
        user = User.objects.all().first()
        link_for_user = _._EmailConfirmationController__generate_link_for_user(  # noqa pylint: disable=C0301,W0212
            user,
            request
        )
        resp = self.client.get(
            link_for_user
        )
        self.assertRedirects(
            resp,
            reverse('successfully_confirmed_email')
        )
        user.refresh_from_db()
        self.assertTrue(
            user.is_active,
            'is_active is not set when user successfully confirmed email'
        )

    def _send_correct_registration_data(self) -> HttpResponse:
        return self.__send_registration_request(
            self.__fill_data_set(
                self.user,
                self.institution,
                self.raw_password
            )
        )

    def __fill_data_set(self, user: User, institution: Institution, raw_password: str):
        data = self._get_form_data()
        data['full_name'] = user.full_name
        data['email'] = user.email
        data['password1'] = raw_password
        data['password2'] = raw_password
        # we are using SecureModelChoiceField to hide all the id`s,
        # so we have to directly hide it here
        data['registration_requests-0-institution'] = hide_int(institution.pk)
        return data

    @classmethod
    def _get_form_data(cls) -> _user_registration_data_dict:
        sample_data = _user_registration_data_dict()  # noqa
        # here we assign values that are always the same in form submission data
        # empty message is included even when user did not write anything
        sample_data['registration_requests-0-message'] = ''
        sample_data['registration_requests-0-id'] = ''
        sample_data['registration_requests-0-user'] = ''
        sample_data['registration_requests-TOTAL_FORMS'] = '1'
        sample_data['registration_requests-INITIAL_FORMS'] = '0'
        sample_data['registration_requests-MIN_NUM_FORMS'] = '1'
        sample_data['registration_requests-MAX_NUM_FORMS'] = '1'
        return sample_data.copy()

    def __send_registration_request(self, data: _user_registration_data_dict) -> HttpResponse:
        return self.client.post(
            reverse_lazy('register'),
            {
                **data
            },
            follow=True
        )
