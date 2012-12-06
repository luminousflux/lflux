from django.test.client import Client
from django.test import TestCase
from lstory.models import Story
from datetime import datetime
import reversion


class BasicFunctionalityTest(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_story_creation(self):
        client = Client()
        with reversion.create_revision():
            Story.objects.create(published=datetime.now(), body='roflcopter', summary='roflcopter', title='roflcopter',slug='roflcopter',name='roflcopter')
        responses = [client.get('/story/roflcopter/'),client.get('/story/roflcopter/embed/')]
        for x in responses:
            self.assertEqual(x.status_code, 200)
