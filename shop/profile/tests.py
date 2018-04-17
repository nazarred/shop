import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile


class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glassonion')

    def test_show_username(self):
        self.client.login(username='john', password='glassonion')
        response = self.client.get('/')
        self.assertContains(response, 'john')

    def test_update_user_without_profile(self):
        self.client.login(username='john', password='glassonion')
        profile_url = '/accounts/profile/'
        response = self.client.post('/accounts/update/', {
            'email': self.user.email,
            'first_name': 'name-test',
            'phone_nmb': '125258',
            'date_of_birth': datetime.date.today()
        })
        self.assertRedirects(response, profile_url)
        self.assertEqual(Profile.objects.all().count(), 1)
        response = self.client.get(profile_url)
        self.assertContains(response, 'name-test')

    def test_update_user_with_profile(self):
        self.client.login(username='john', password='glassonion')
        profile_url = '/accounts/profile/'
        profile = Profile.objects.create(
            user=self.user,
            phone_nmb='125258',
            date_of_birth=datetime.date.today()
        )
        response = self.client.get(profile_url)
        self.assertContains(response, '125258')
        response = self.client.post('/accounts/update/', {
            'email': self.user.email,
            'first_name': 'name-test',
            'phone_nmb': '066-345-3285',
            'date_of_birth': datetime.date.today()
        })
        self.assertEqual(Profile.objects.all().count(), 1)
        response = self.client.get(profile_url)
        self.assertContains(response, 'name-test')
        self.assertContains(response, '066-345-3285')
