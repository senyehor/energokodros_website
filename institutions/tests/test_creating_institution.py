from django.test import TestCase
from django.urls import reverse_lazy
from faker import Faker

from institutions.models import Facility
from users.tests.factories import create_admin_client


class InstitutionCreationTest(TestCase):
    def setUp(self):
        self.client = create_admin_client()
        self.creation_url = reverse_lazy('new-institution')
        fake = Faker()
        self.institution_name = fake.name()
        self.institution_description = fake.text(max_nb_chars=200)

    def test_creating_institution(self):
        resp = self.client.post(
            self.creation_url,
            data={
                'name':        self.institution_name,
                'description': self.institution_description
            },
            follow=True
        )
        self.assertEqual(
            resp.status_code,
            200,
            'invalid return code with correct data'
        )
        self.assertTrue(
            Facility.objects.filter(
                name=self.institution_name,
                description=self.institution_description
            ).count() == 1,
            'Institution not created or created multiple'
        )
