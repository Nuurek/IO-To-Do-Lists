from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from unittest.mock import patch
from functools import partial
from typing import Callable

from superlists.tests import (
    create_todo_list
)
from .models import UserProfile
from .forms import RegisterForm


TEST_USERNAME = 'test_user'
TEST_EMAIL = 'test_user@test.test'
TEST_PASSWORD = 'test123'


def create_user_profile(username, email, password):
    """
    Create new activated UserProfile with given username, email and password.

    Attributes:
        username - user's name
        email - user's email address
        password - user's password
    """
    user = User.objects.create_user(username, email, password)
    return UserProfile.objects.create(user=user, confirmation_code=get_random_string(32))


create_test_user_profile: Callable[[], UserProfile] = partial(
    create_user_profile, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD
)


class UserProfileViewTest(TestCase):
    """
    Collection of tests for UserProfileView class.
    """

    def test_user_not_logged_in(self):
        """
        Getting user profile without logging in should return 404.
        """
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_no_todo_lists(self):
        """
        UserProfile view without todo lists should be empty.
        """
        create_test_user_profile()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lists are available.")

    def test_with_todo_lists(self):
        """
        UserProfile view with todo lists should display the lists.
        """
        user_profile = create_test_user_profile()
        create_todo_list("Test todo list", False, user_profile=user_profile)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test todo list")


class LoginViewTest(TestCase):
    """
    Collection of tests for user_login method.
    """

    def setUp(self):
        self.user_profile = create_test_user_profile()
        self.credentials = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
        }

    def test_login_correct(self):
        """
        Login attempt with correct credentials should succeed.
        """
        url = reverse("login")
        response = self.client.post(url, self.credentials, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertContains(response, TEST_USERNAME)

    def test_login_incorrect_username(self):
        """
        Login attempt with incorrect username should not succeed.
        """
        self.credentials['username'] += "XD"
        url = reverse("login")
        response = self.client.post(url, self.credentials, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertNotContains(response, TEST_USERNAME)
        self.assertContains(response, "Username or password incorrect")

    def test_login_incorrect_password(self):
        """
        Login attempt with incorrect password should not succeed.
        """
        self.credentials['password'] += "XD"
        url = reverse("login")
        response = self.client.post(url, self.credentials, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertNotContains(response, TEST_USERNAME)
        self.assertContains(response, "Username or password incorrect")

    def test_login_inactive_user(self):
        """
        Login attempt for inactive user should not succeed.
        """
        self.user_profile.user.is_active = False
        self.user_profile.user.save()
        url = reverse("login")
        response = self.client.post(url, self.credentials, follow=True)
        self.assertNotContains(response, TEST_USERNAME)
        self.assertContains(response, "Username or password incorrect")

    def test_login_inactive_user_redirects_to_home_page(self):
        self.user_profile.user.is_active = False
        self.user_profile.user.save()
        url = reverse("login")
        response = self.client.post(url, self.credentials, follow=True)
        self.assertRedirects(response, reverse("index"))

    def test_login_get(self):
        """
        GET on login page should redirect to index.
        """
        url = reverse("login")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse("index"))


class LogoutViewTest(TestCase):
    """
    Collection of tests for user_logout method.
    """

    def test_logout_user_not_logged(self):
        """
        Logout attempt without logging in should redirect to index.
        """
        url = reverse("logout")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse("index"))

    def test_logout_user_logged(self):
        """
        Logout attempt with user logged in should succeed.
        """
        create_test_user_profile()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        url = reverse("logout")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertNotContains(response, TEST_USERNAME)


class ConfirmViewTest(TestCase):
    """
    Collection of tests for RegisterConfirmView class.
    """

    def setUp(self):
        self.user_profile = create_test_user_profile()
        self.user_profile.user.is_active = False
        self.user_profile.user.save()

    def test_valid_confirm_code(self):
        """
        Using valid confirmation code should activate inactive user.
        """
        url = reverse("register_confirm", args=(
            self.user_profile.id, self.user_profile.confirmation_code,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.user_profile.user.refresh_from_db()
        self.assertTrue(self.user_profile.user.is_active)

    def test_invalid_confirmation_code(self):
        """
        Using invalid confirmation code should not activate inactive user.
        """
        url = reverse("register_confirm", args=(
            self.user_profile.id, get_random_string(32),))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.user_profile.user.refresh_from_db()
        self.assertFalse(self.user_profile.user.is_active)


class RegisterViewTest(TestCase):

    @patch('django.contrib.auth.models.User.email_user')
    def test_is_confirmation_code_in_sent_email(self, mock_email_user_method):
        form = {
            'username': TEST_USERNAME,
            'email': TEST_EMAIL,
            'password': TEST_PASSWORD,
            'confirm_password': TEST_PASSWORD
        }
        url = reverse('register')
        self.client.post(url, form)
        created_profile = UserProfile.objects.get(user__username=TEST_USERNAME)
        confirmation_code = created_profile.confirmation_code
        called_argument = mock_email_user_method.call_args_list[0][0][1]
        self.assertTrue(confirmation_code in called_argument)
