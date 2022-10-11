from typing import TypedDict

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from institutions.models import Facility
from institutions.tests.factories import InstitutionFactory
from users.logic.user_registration_controller import _EmailConfirmationController  # noqa
from users.models import UserRoleApplication
from users.tests.factories import UserFactory
from utils.forms import hash_id

User = get_user_model()


class UserRegistrationTest(TestCase):
    _user_registration_data_dict = TypedDict(
        '_user_registration_data_dict',
        {
            'full_name':   str,
            'email':       str,
            'password1':   str,
            'password2':   str,
            'institution': str,
            'message':     str,
        }
    )

    def setUp(self):
        self.client = Client()
        self.raw_password = '%tv{,,E)36'
        self.message = 'some message'
        self.user: User = UserFactory.build(password=self.raw_password)
        self.institution = InstitutionFactory()

    def test_with_correct_data_set(self):
        resp = self.send_correct_registration_data()
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

    def test_user_and_role_application_is_created_correctly(self):
        self.send_correct_registration_data()
        user = User.objects.get(
            full_name=self.user.full_name,
            email=self.user.email
        )
        self.assertFalse(
            user.is_active,
            'user must me inactive on registration (email unconfirmed)'
        )
        user_role_application = UserRoleApplication.objects.get(
            user=user
        )
        self.assertEqual(
            user_role_application.institution,
            self.institution,
            'registration request is set for wrong institution'
        )

    def test_email_confirmation(self):
        self.send_correct_registration_data()
        # here we mock request just to use it`s is_secure and get_host methods to generate link
        request = RequestFactory().get('')
        # here we get just first user, as it should be created and be the only one
        user = User.objects.all().first()
        _ = _EmailConfirmationController
        # pylint: disable-next=W0212
        link_for_user = _._EmailConfirmationController__generate_link_for_user(  # noqa
            user,
            request
        )
        resp = self.client.get(
            link_for_user
        )
        self.assertTemplateUsed(
            resp,
            'registration/successfully_confirmed_email.html',
            'needed template is not used'
        )
        user.refresh_from_db()
        self.assertTrue(
            user.is_active,
            'is_active is not set when user successfully confirmed email'
        )

    def send_correct_registration_data(self) -> HttpResponse:
        return self.send_registration_request(
            self.user,
            self.institution,
            self.raw_password
        )

    def __complete_data(self, user: User, institution: Facility, raw_password: str):
        data = self.__get_form_data()
        data['full_name'] = user.full_name
        data['email'] = user.email
        data['password1'] = raw_password
        data['password2'] = raw_password
        data['institution'] = hash_id(institution.pk)
        return data

    def __get_form_data(self) -> _user_registration_data_dict:
        # when field is not filled it is sent with empy data anyway
        data = {
            'message': ''
        }
        data = self._user_registration_data_dict(
            **data
        )
        return data

    def send_registration_request(
            self, user: User, institution: Facility, raw_password: str) -> HttpResponse:
        return self.client.post(
            reverse('register'),
            {
                **self.__complete_data(user, institution, raw_password)
            },
            follow=True
        )
