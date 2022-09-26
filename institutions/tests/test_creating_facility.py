from django.test import TestCase
from django.urls import reverse
from faker import Faker

from administrator.tests.factories import create_admin_client
from institutions.models import Facility
from utils.forms import _hide_id  # noqa


class FacilityCreationTest(TestCase):
    def setUp(self):
        self.client = create_admin_client()
        self.creation_url = reverse('new-facility')
        fake = Faker()
        self.parent_facility: Facility = Facility.add_root(
            name=fake.name, description=fake.text(max_nb_chars=200)
        )
        self.facility_name = fake.name()
        self.facility_description = fake.text(max_nb_chars=200)

    def test_creating_facility(self):
        parent_facility_id = _hide_id(
            self.parent_facility.pk
        )
        response = self.client.post(
            self.creation_url,
            data={
                'name':            self.facility_name,
                'description':     self.facility_description,
                'parent_facility': parent_facility_id
            },
            follow=True
        )
        self.assertEqual(
            response.status_code,
            200,
            'invalid response code with correct data'
        )
        created_facility = Facility.objects.get(
            name=self.facility_name,
            description=self.facility_description,
        )
        self.parent_facility.refresh_from_db()
        self.assertTrue(
            created_facility.is_child_of(self.parent_facility),
            'parent facility is set incorrectly'
        )
