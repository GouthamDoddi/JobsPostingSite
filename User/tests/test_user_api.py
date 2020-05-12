from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status

CREATE_USER_URL = reverse('User:create')
TOKEN_URL = reverse('User:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the user's api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user with valid payload(credentials) is
        successful"""
        payload = {
            'email': 'testhahah@gmail.com',
            'password': 'testing123',
            'name': 'test man',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertNotIn('password', res.data)
        self.assertTrue(user.check_password(payload['password']))

    def test_user_exists(self):
        """Test creating user that already exits fails"""
        payload = {'email': 'testman5555@email.com', 'password': 'testing123'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test the password is more then 5 characters"""
        payload = {'email': 'testman@email.com', 'password': '123'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test that token si created for the user"""
        payload = {'email': 'testman5555@email.com', 'password': 'testing123'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        print("this is the token {}".format(res.data))

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_invalid_credentials(self):
        """Test that token is not create with invalid credentials"""
        create_user(email='testman@mans.com', password='testpass')
        payload = {'email': 'testman@mans.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if the user doesn't exist"""
        payload = {'email': 'testman5555@email.com', 'password': 'testing123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that token can't be created with missing field"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
