from django.test import Client

from users.tests.factories import UserFactory


def create_admin_client() -> Client:
    client = Client()
    client.force_login(UserFactory(is_admin=True))
    return client
