from enum import Enum
from typing import TypedDict

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from faker import Faker

from administrator.tests.factories import create_admin_client
from institutions.models import Facility
from users.models import UserRole, UserRoleApplication
from users.tests.factories import UserRoleApplicationFactory
from utils.forms import SecureModelChoiceField


class UserRoleApplicationDetailTest(TestCase):
    class _DECISIONS(Enum):
        ACCEPT = 'accept'
        DECLINE = 'decline'

    _user_role_application_decision_data_dict = TypedDict(
        '_user_role_application_decision_data_dict',
        {
            'decision':             _DECISIONS,  # noqa
            'message_for_user':     str,
            'position':             str,
            'user':                 str,
            'institution':          str,
            'object_has_access_to': str
        }
    )

    def setUp(self):
        self.admin_client = create_admin_client()
        self.user_role_application = UserRoleApplicationFactory()
        self.object_has_access_to = self.user_role_application.institution
        fake = Faker()
        self.position_to_grant_user: str = fake.text(max_nb_chars=20)

    def test_accepting_application(self):
        resp = self.send_decision(
            decision=self._DECISIONS.ACCEPT,
            object_has_access_to=self.user_role_application.institution,
            position=self.position_to_grant_user
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
                object_has_access_to=self.user_role_application.institution,
                position=self.position_to_grant_user
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
            object_has_access_to: Facility = None, position: str = None) -> HttpResponse:
        return self.admin_client.post(
            reverse(
                'user-role-application-decision',
                kwargs={'pk': self.user_role_application.pk}
            ),
            {
                **self.__complete_data(
                    decision.value,
                    position,
                    object_has_access_to
                )
            },
            follow=True
        )

    def __complete_data(
            self, decision: str,
            position: str | None, object_has_access_to: Facility | None):
        complete_data = self.__get_form_data()
        complete_data['decision'] = decision
        # when declining application neither position nor object_has_access_to
        # have to be filled in form, so they are just ''
        complete_data['position'] = position if position else ''
        hashed_id_or_empty_string = (
            SecureModelChoiceField._hide_id(object_has_access_to.pk)  # pylint: disable=W0212
            if object_has_access_to
            else ''
        )
        complete_data['object_has_access_to'] = hashed_id_or_empty_string
        return complete_data

    def __get_form_data(self) -> _user_role_application_decision_data_dict:
        # here we have to set data as if it was pre-populated by form
        user_id_hashed = SecureModelChoiceField._hide_id(self.user_role_application.user.pk)  # pylint: disable=W0212
        data = {
            'message_for_user': '',
            'user':             user_id_hashed
            # noqa pylint: disable=W0212
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
