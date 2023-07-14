from typing import Literal, TypedDict

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from faker import Faker

from institutions.models import AccessLevel
from institutions.tests.factories import AccessLevelFactory
from users.models import UserRole, UserRoleApplication
from users.tests.factories import UserFactory, UserRoleApplicationRequestFactory
from utils.for_tests_only import hide_id

fake = Faker()

_decision = Literal['accept', 'decline']
_user_role_application_decision_data_dict = TypedDict(
    'data_dict',  # noqa
    {
        'decision':         _decision,
        'message_for_user': str,
        'position':         str,
        'access_level':     str,
        'user':             str,
        'institution':      str,
    }
)


class UserRoleApplicationDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.force_login(UserFactory(is_admin=True))
        self.user_role_application = UserRoleApplicationRequestFactory()
        self.access_level = AccessLevelFactory()
        self.position: str = fake.words()

    def test_accepting_application(self):
        resp = self.send_decision(
            'accept',
            self.position,
            self.access_level
        )
        self.assertEqual(
            200,
            resp.status_code,
            'error while accepting user application'
        )
        self.assertRedirects(
            resp,
            reverse_lazy('users_roles_applications'),
        )
        try:
            UserRole.objects.get(
                user=self.user_role_application.user,
                institution=self.user_role_application.institution,
                access_level=self.access_level
            )
        except ObjectDoesNotExist:
            assert False, 'user role is not created even though response status code is 200'
        self.__check_user_application_is_deleted()

    def test_declining_application(self):
        resp = self.send_decision(
            'decline'
        )
        self.assertEqual(
            200,
            resp.status_code,
            'error while declining user application'
        )
        self.assertRedirects(
            resp,
            reverse_lazy('users_roles_applications'),
        )
        self.__check_user_application_is_deleted()

    def send_decision(
            self, decision: _decision, position: str = '',
            access_level: AccessLevel = None) -> HttpResponse:
        return self.client.post(
            reverse('user_role_application', kwargs={'pk': self.user_role_application.pk}),
            {
                **self.__complete_data(
                    decision=decision,
                    position=position,
                    access_level=access_level
                )
            },
            follow=True
        )

    def __complete_data(self, decision: _decision, position: str, access_level: AccessLevel):
        complete_data = self.__get_form_data()
        complete_data['decision'] = decision
        complete_data['position'] = position
        # ignoring access_level when declining
        complete_data['access_level'] = hide_id(access_level.pk) if access_level else ''
        return complete_data

    def __get_form_data(self) -> _user_role_application_decision_data_dict:
        # here we have to set data as if it was pre-populated by form
        data = {
            'message_for_user': '',
            'user':             hide_id(self.user_role_application.user.pk),
            'institution':      hide_id(self.user_role_application.institution.pk)
        }
        data = _user_role_application_decision_data_dict(**data)
        return data

    def __check_user_application_is_deleted(self):
        self.assertFalse(
            UserRoleApplication.objects.filter(
                user=self.user_role_application.user,
                institution=self.user_role_application.institution,
            ).exists(),
            'user role application is not deleted'
        )
