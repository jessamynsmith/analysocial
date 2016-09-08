from django.test import TestCase

from libs import helpers
from django.contrib.auth import get_user_model


class TestGetFullDomain(TestCase):

    def test_http(self):
        result = helpers.get_full_domain()
        self.assertEqual('http://example.com', result)

    def test_https(self):
        with self.settings(SECURE_SSL_REDIRECT=True):
            result = helpers.get_full_domain()
            self.assertEqual('https://example.com', result)


class TestWriteCsv(TestCase):
    maxDiff = None

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            password='bogus', email='jessamyn1@example.com', username=u'jessamyn1')
        self.user2 = get_user_model().objects.create_user(
            password='bogus', email='jessamyn2@example.com', username=u'jessamyn2')

    def test_create_csv_empty(self):
        queryset = get_user_model().objects.filter(username='does_not_exist')
        result = helpers.create_csv(queryset)
        self.assertEqual(b'', result.getvalue())

    def test_create_csv(self):
        queryset = get_user_model().objects.all().values('username', 'email')
        result = helpers.create_csv(queryset)

        expected = (b'email,username\r\n'
                    b'jessamyn1@example.com,jessamyn1\r\n'
                    b'jessamyn2@example.com,jessamyn2\r\n')
        self.assertEqual(expected, result.getvalue())
