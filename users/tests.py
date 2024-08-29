from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTest(TestCase):
    def test_user_account_is_create(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'azamat',
                'first_name': 'azamat1',
                'last_name': 'berdimurodov',
                'email': 'azamat@gmail.com',
                'password': 'azamat1234'
            }
        )

        user = CustomUser.objects.get(username='azamat')

        self.assertEquals(user.first_name, 'azamat1')
        self.assertEquals(user.last_name, 'berdimurodov')
        self.assertEquals(user.email, 'azamat@gmail.com')
        self.assertNotEquals(user.password, 'azamat1234')
        self.assertTrue(user.check_password('azamat1234'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'last_name': 'azamat1',
                'email': 'azamat@gmail.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEquals(user_count, 0)
        form = response.context['form']
        self.assertFormError(form, "username", "This field is required.")
        self.assertFormError(form, 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'azamat',
                'first_name': 'azamat1',
                'last_name': 'berdimurodov',
                'email': 'azamat',
                'password': 'azamat1234'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEquals(user_count, 0)
        form = response.context['form']
        self.assertFormError(form, "email", "Enter a valid email address.")

    def test_unique_username(self):
        CustomUser.objects.create(username='azamat', last_name='berdimurodov', password='azamat1234')
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'azamat',
                'first_name': 'azamat1',
                'last_name': 'berdimurodov',
                'email': 'azamat@gmail.com',
                'password': 'azamat1234'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEquals(user_count, 1)
        form = response.context['form']
        self.assertFormError(form, 'username', 'A user with that username already exists.')


class LoginTest(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='abduqodir')
        self.db_user.set_password('kiber4224')
        self.db_user.save()

    def test_successfully_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username':'abduqodir',
                'password':'kiber4224'
            }
        )

        self.assertTrue(self.db_user.is_authenticated)

    def test_wrong_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'azamat1',
                'password': 'kiber4224'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_wrong_password_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'abduqodir',
                'password': 'kiber1234'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_redirect_login(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('users:login')+"?next="+reverse('users:profile'))

    def test_profile_detail(self):
        user = CustomUser.objects.create(
            username='abduqodir',
            first_name='abduq',
            last_name='dusmurodov',
            email='hackinge33@gmail.com'
        )
        user.set_password('kiber4224')
        user.save()

        self.client.login(username='abduqodir', password='kiber4224')
        response=self.client.get(reverse('users:profile'))

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)


class LogoutTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='abduqodir',
            first_name='abduq',
            last_name='dusmurodov',
            email='hackinge33@gmail.com'
        )
        self.user.set_password('kiber4224')
        self.user.save()

    def test_successfully_logout(self):
        self.client.login(username='abduqodir', password='kiber4224')

        response = self.client.get(reverse('users:logout'))

        user1 = get_user(self.client)
        self.assertEquals(response.url, reverse('landing_page'))
        self.assertFalse(user1.is_authenticated)


class ProfileUpdateTestCase(TestCase):
    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='abduqodir',
            first_name='abduqodirbek',
            last_name='dusmurodov',
            email='hackinge33@gmail.com'
        )
        user.set_password('kiber4224')
        user.save()

        self.client.login(username='abduqodir', password='kiber4224')

        response=self.client.post(
            reverse("users:profile-edit"),
            data={
                'username':'azamat',
                'first_name':'azamatbek',
                'last_name':'berdimurodov',
                'email':'azamat1@gmail.com'
            }
        )
        user = CustomUser.objects.get(id=user.id)

        self.assertEquals(user.username, 'azamat')
        self.assertEquals(user.first_name, 'azamatbek')
        self.assertEquals(user.last_name, 'berdimurodov')
        self.assertEquals(user.email, 'azamat1@gmail.com')
        self.assertEquals(response.url, reverse('users:profile'))
        self.assertEquals(response.status_code, 302)
