import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glassonion')

    def test_redirect_login(self):
        response = self.client.post('/login/', {'login': 'nazar', 'password': 'w4uredko'})
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
        self.assertTrue(user.get().is_authenticated)
