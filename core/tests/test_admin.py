from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminUserModel(TestCase):

    def setUp(self):
        """This method will make all the required setup
         like creating client and user"""
        self.client = Client()
        self.super_user = get_user_model().objects.create_superuser(
            'superman@email.com', 'testing123')
        self.client.force_login(self.super_user)
        self.user = get_user_model().objects.create_user(email='testman@email.com',
                                                         password='testing123', name='test man here for test')

    def test_if_users_are_listed_in_admin(self):
        """This method checks if new users are listed in 
        the admin page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user info works by testing user
        change page"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the user can be created by testing user
               change page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)
