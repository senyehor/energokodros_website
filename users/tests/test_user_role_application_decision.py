from enum import Enum
from typing import TypedDict

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from faker import Faker

from institutions.models import Facility
from users.models import UserRole, UserRoleApplication
from users.tests.factories import create_admin_client, UserRoleApplicationFactory
from utils.common import hash_id


class UserRoleApplicationDetailTest(TestCase):
    class _DECISIONS(Enum):
        ACCEPT = 'accept'
        DECLINE = 'decline'

    _user_role_application_decision_data_dict = TypedDict(
        '_user_role_application_decision_data_dict',
        {
            'decision':               _DECISIONS,  # noqa
            'message_for_user':       str,
            'position_name':          str,
            'user':                   str,
            'institution':            str,
            'facility_has_access_to': str
        }
    )

    def setUp(self):
        self.admin_client = create_admin_client()
        self.user_role_application = UserRoleApplicationFactory()
        self.facility_has_access_to = self.user_role_application.institution
        fake = Faker()
        self.position_to_grant_user: str = fake.text(max_nb_chars=20)

    def test_accepting_application(self):
        resp = self.send_decision(
            decision=self._DECISIONS.ACCEPT,
            facility_has_access_to=self.user_role_application.institution,
            position_name=self.position_to_grant_user,
        )
        self.assertEqual(
            200,
            resp.status_code,
            'error while accepting user application'
        )
        self.assertRedirects(
            resp,
            reverse_lazy('users-roles-applications'),
        )
        try:
            UserRole.objects.get(
                user=self.user_role_application.user,
                facility_has_access_to=self.user_role_application.institution,
                position_name=self.position_to_grant_user
            )
        except ObjectDoesNotExist:
            assert False, 'user role is not created even though response status code is 200'
        self.__check_user_application_is_deleted()

    def test_declining_application(self):
        resp = self.send_decision(
            self._DECISIONS.DECLINE
        )
        self.assertEqual(
            200,
            resp.status_code,
            'error while declining user application'
        )
        self.assertRedirects(
            resp,
            reverse_lazy('users-roles-applications'),
        )
        self.__check_user_application_is_deleted()

    def send_decision(
            self, decision: _DECISIONS,
            facility_has_access_to: Facility = None, position_name: str = None) -> HttpResponse:
        return self.admin_client.post(
            reverse(
                'user-role-application-decision',
                kwargs={'pk': self.user_role_application.pk}
            ),
            {
                **self.__complete_data(
                    decision.value,
                    position_name,
                    facility_has_access_to
                )
            },
            follow=True
        )

    def __complete_data(
            self, decision: str,
            position_name: str | None, facility_has_access_to: Facility | None):
        complete_data = self.__get_form_data()
        complete_data['decision'] = decision
        # when declining application neither position nor facility_has_access_to
        # have to be filled in form, so they are just ''
        complete_data['position_name'] = position_name if position_name else ''
        hashed_id_or_empty_string = (
            hash_id(facility_has_access_to)
            if facility_has_access_to
            else ''
        )
        complete_data['facility_has_access_to'] = hashed_id_or_empty_string
        return complete_data

    def __get_form_data(self) -> _user_role_application_decision_data_dict:
        # here we set data as if it was pre-populated by form
        user_id_hashed = hash_id(self.user_role_application.user)
        data = {
            'message_for_user': '',
            'user':             user_id_hashed
        }
        data = self._user_role_application_decision_data_dict(**data)
        return data

    def __check_user_application_is_deleted(self):
        self.assertFalse(
            UserRoleApplication.objects.filter(
                user=self.user_role_application.user,
                institution=self.user_role_application.institution,
            ).exists(),
            'user role application is not deleted'
        )
