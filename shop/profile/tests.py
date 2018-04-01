import datetime

from django.contrib import auth
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glassonion')

    def test_redirect_login(self):
        response = self.client.post('/login/', {'login': 'john', 'password': 'glassonion'})
        client_user = auth.get_user(self.client)
        self.assertTrue(client_user.is_authenticated())
        self.assertRedirects(response, '/')

    def test_show_username(self):
        self.client.login(username='john', password='glassonion')
        response = self.client.get('/')
        self.assertContains(response, 'john')

    def test_redirect_authuser(self):
        response = self.client.get('/profile/registration/')
        self.assertTemplateUsed(response, 'profile/register.html')
        self.client.login(username='john', password='glassonion')
        response = self.client.get('/profile/registration/')
        self.assertRedirects(response, '/')

    def test_registration_view(self):
        test_user = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@mail.com',
            'password': 'asdrtew19',
            'password1': 'asdrtew19',
            'phone_nmb': '123012345678925',  # номер телефону ведений не коректно(макс довжина 12 символів)
            'date_of_birth': datetime.date.today()
        }
        # спочатку перевіряємо з некоректними даними для ProfileForm.phone_nmb
        response = self.client.post('/profile/registration/', test_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="messages"')
        # тепер вводимо коректні дані
        test_user['phone_nmb'] = 12345
        response = self.client.post('/profile/registration/', test_user)
        profile_nmb = Profile.objects.all().count()
        user = User.objects.filter(username='test')
        self.assertRedirects(response, '/')
        self.assertEqual(profile_nmb, 1)
        self.assertEqual(profile_nmb, user.count())
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_change_password(self):
        self.client.login(username='john', password='glassonion')
        response = self.client.post('/profile/update/password/1/', {
            'old_password': 'glassonion',
            'new_password1': 'test1298',
            'new_password2': 'test1298'
        })
        self.assertRedirects(response, '/')
        self.assertFalse(auth.get_user(self.client).is_authenticated())
        self.client.login(username='john', password='test1298')
        self.assertTrue(auth.get_user(self.client).is_authenticated())

    def test_update_user_without_profile(self):
        self.client.login(username='john', password='glassonion')
        profile_url = '/profile/detail/%d/' % self.user.id
        response = self.client.post('/profile/update/%d/' % self.user.id, {
            'username': self.user.username,
            'email': self.user.email,
            'first_name': 'name-test',
            'phone_nmb': '125258',
            'date_of_birth': datetime.date.today()
        })
        # import pdb; pdb.set_trace()
        self.assertRedirects(response, profile_url)
        self.assertEqual(Profile.objects.all().count(), 1)
        response = self.client.get(profile_url)
        self.assertContains(response, 'name-test')

    def test_update_user_with_profile(self):
        self.client.login(username='john', password='glassonion')
        profile_url = '/profile/detail/%d/' % self.user.id
        profile = Profile.objects.create(
            user=self.user,
            phone_nmb='125258',
            date_of_birth=datetime.date.today()
        )
        response = self.client.get(profile_url)
        self.assertContains(response, '125258')
        response = self.client.post('/profile/update/%d/' % self.user.id, {
            'username': self.user.username,
            'email': self.user.email,
            'first_name': 'name-test',
            'phone_nmb': '066-345-3285',
            'date_of_birth': datetime.date.today()
        })
        self.assertRedirects(response, profile_url)
        self.assertEqual(Profile.objects.all().count(), 1)
        response = self.client.get(profile_url)
        self.assertContains(response, 'name-test')
        self.assertContains(response, '066-345-3285')
