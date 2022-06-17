from django.test import TestCase

from accounts.tests.factories import create_user


class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = create_user(email='testemail1@example.com', create_token=False)

        assert user
        assert user.username == 'testuser'
        assert user.email == 'testemail1@example.com'
