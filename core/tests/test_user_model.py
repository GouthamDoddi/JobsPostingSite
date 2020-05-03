from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):

    def test_User_creation(self):
        """Test if the user model is working"""
        email = 'testmail@email.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(email=email, password=password)
        # now check if the credentials match
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalize(self):
        """Test the email for a new user is normalized"""
        email = 'newuser@EMAIL.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_raise_error_for_no_email(self):
        """Make sure that passing no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        """Testing if we can create a super user"""
        user = get_user_model().objects.create_superuser('testmail@email.com',
                                                         'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
