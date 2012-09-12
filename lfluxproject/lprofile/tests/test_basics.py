from django.test.client import Client
from django.test import TestCase


class BasicFunctionalityTest(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
