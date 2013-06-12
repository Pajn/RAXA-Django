'''
Copyright (C) 2013 Rasmus Eneman <rasmus@eneman.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import json
from django.test.client import Client
from django.utils import unittest
from backend.authorization import get_user
from .views import API_VERSION, RAXA_VERSION


class ApiTestCase(unittest.TestCase):

    def test_empty_request(self):
        """
        An empty request shouldn't generate any errors and should provide all required fields.
        """
        c = Client()
        response = c.get('/api/')
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'ok')
        self.assertEqual(data['status']['errors'], [])
        self.assertEqual(data['status']['version']['RAXA'], RAXA_VERSION)
        self.assertEqual(data['status']['version']['api'], API_VERSION)
        self.assertEqual(data['response'], {})

    def test_login_request(self):
        """
        Test that the login works and returns an api key
        """
        user = get_user()
        user.set_password('test')

        c = Client()
        response = c.get('/api/login/', {'password': 'test'})
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'ok')
        self.assertTrue('key' in data['response'])

    def test_login_request_with_bad_password(self):
        """
        Test that the login works and don't returns an api key on bad passwords
        """
        user = get_user()
        user.set_password('test')

        c = Client()
        response = c.get('/api/login/', {'password': 'test2'})
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'error')
        self.assertEqual(data['status']['errors'], ['Bad Password'])
        self.assertFalse('key' in data['response'])

    def test_bad_login_request(self):
        """
        Bad requests should return errors and don't create a crash or 500 page
        """
        c = Client()
        response = c.get('/api/login/')
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'error')
        self.assertEqual(data['status']['errors'], ['NotSet:password'])

    def test_bad_device_request(self):
        """
        Bad requests should return errors and don't create a crash or 500 page
        """
        c = Client()
        response = c.get('/api/device/')
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'error')
        self.assertEqual(data['status']['errors'], ['NotSet:id'])

        response = c.get('/api/device/', {'id': 5})
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'error')
        self.assertEqual(data['status']['errors'], ['NotSet:action'])

        response = c.get('/api/device/', {'id': None, 'action': 'on'})
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'error')
        self.assertEqual(data['status']['errors'], ['InvalidValue:id'])

    def test_bad_scenario_request(self):
        """
        Bad requests should return errors and don't create a crash or 500 page
        """
        c = Client()
        response = c.get('/api/scenario/')
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'error')
        self.assertEqual(data['status']['errors'], ['NotSet:id'])

        response = c.get('/api/scenario/', {'id': None})
        data = json.loads(response.content)

        self.assertEqual(data['status']['status'], 'error')
        self.assertEqual(data['status']['errors'], ['InvalidValue:id'])
