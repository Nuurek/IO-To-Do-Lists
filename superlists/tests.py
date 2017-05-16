from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from .models import ToDoList, ToDoListItem, UserProfile


def create_todo_list(name, is_private, user_profile=None):
    """
    Create new ToDoList at present time and add it to database.

    Attributes:
        name - name of the list
        private - should list be displayed on main page
    """
    return ToDoList.objects.create(name=name, creation_date=timezone.now(), is_private=is_private, user_profile=user_profile)


def create_todo_list_item(name, completed, todo_list):
    """
    Create new ToDo List Item for given ToDo List.

    Attributes:
        name - name of the item
        completed - whether item is completed
        todo_list - ToDo List to which item belongs
    """
    return ToDoListItem.objects.create(name=name, completed=completed, todo_list=todo_list)


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


class IndexViewTests(TestCase):
    """
    Collection of tests for PublicToDoListListView class.
    """

    def test_recent_todo_list_private(self):
        """
        Recent private ToDo List should not be displayed on main page.
        """
        create_todo_list("Test", True)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lists are available.")

    def test_recent_todo_list_public(self):
        """
        Recent public ToDo List should be displayed on main page.
        """
        create_todo_list("Test todo list", False)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test todo list")


class DetailViewTests(TestCase):
    """
    Collection of tests for ToDoListDetailView class.
    """

    def test_empty_todo_list(self):
        """
        Empty ToDo List should have no tasks displayed on detailed view.
        """
        todo_list = create_todo_list("Test todo list", False)
        url = reverse("list", args=(todo_list.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "list_group_item")

    def test_adding_new_todo_list_item(self):
        """
        Task should be displayed on a ToDo List detailed view.
        """
        create_todo_list("Test todo list", False)
        todo_list = create_todo_list("Test todo list", False)
        task = create_todo_list_item("Test todo list item", False, todo_list)
        url = reverse("list", args=(todo_list.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test todo list item")


class DeleteToDoListViewTest(TestCase):
    """
    Collection of tests for ToDoListDeleteView class.
    """

    def test_delete_todo_list(self):
        """
        Getting todo list view after deleting should return 404.
        """
        todo_list = create_todo_list("Test todo list", False)
        url = reverse("delete_list", args=(todo_list.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url)
        with self.assertRaises(ToDoList.DoesNotExist):
            self.assertEqual(ToDoList.objects.get(id=todo_list.id), None)
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_list(self):
        """
        Trying to delete nonexistent list should result in 404.
        """
        url = reverse("delete_list", args=(0,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class DeleteToDoListItemViewTest(TestCase):
    """
    Collection of tests for ToDoListItemDeleteView class.
    """

    def test_delete_todo_list_item(self):
        """
        Task should not be displayed after being deleted.
        """
        todo_list = create_todo_list("Test todo list", False)
        task = create_todo_list_item("Test todo list item", False, todo_list)
        url = reverse("delete_item", args=(todo_list.id, task.id))
        response = self.client.get(url)
        self.assertRedirects(response, reverse("list", args=(todo_list.id,)))
        url = reverse("list", args=(todo_list.id,))
        response = self.client.get(url)
        with self.assertRaises(ToDoListItem.DoesNotExist):
            self.assertEqual(ToDoListItem.objects.get(id=task.id), None)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test todo list item")

    def test_delete_nonexistent_item(self):
        """
        Trying to delete nonexistent item should result in 404.
        """
        todo_list = create_todo_list("Test todo list", False)
        url = reverse("delete_item", args=(todo_list.id, 0))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


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
        username = "testuser"
        email = "testuser@test"
        password = "test"
        create_user_profile(username, email, password)
        self.client.login(username=username, password=password)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No lists are available.")

    def test_with_todo_lists(self):
        """
        UserProfile view with todo lists should display the lists.
        """
        username = "testuser"
        email = "testuser@test"
        password = "test"
        user_profile = create_user_profile(username, email, password)
        create_todo_list("Test todo list", False, user_profile=user_profile)
        self.client.login(username=username, password=password)
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test todo list")


class LoginViewTest(TestCase):
    """
    Collection of tests for user_login method.
    """

    username = "testuser"
    email = "testuser@test"
    password = "test"
    user_profile = None

    def setUp(self):
        self.user_profile = create_user_profile(
            self.username, self.email, self.password)

    def test_login_correct(self):
        """
        Login attempt with correct credentials should succeed.
        """
        arguments = {
            "username": self.username,
            "password": self.password
        }
        url = reverse("login")
        response = self.client.post(url, arguments, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertContains(response, self.username)

    def test_login_incorrect_username(self):
        """
        Login attempt with incorrect username should not succeed.
        """
        arguments = {
            "username": self.username.join("XD"),
            "password": self.password
        }
        url = reverse("login")
        response = self.client.post(url, arguments, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertNotContains(response, self.username)
        self.assertContains(response, "Username or password incorrect")

    def test_login_incorrect_password(self):
        """
        Login attempt with incorrect password should not succeed.
        """
        arguments = {
            "username": self.username,
            "password": self.password.join("XD")
        }
        url = reverse("login")
        response = self.client.post(url, arguments, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertNotContains(response, self.username)
        self.assertContains(response, "Username or password incorrect")

    def test_login_inactive_user(self):
        """
        Login attempt for inactive user should not succeed.
        """
        self.user_profile.user.is_active = False
        self.user_profile.user.save()
        arguments = {
            "username": self.username,
            "password": self.password
        }
        url = reverse("login")
        response = self.client.post(url, arguments, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertNotContains(response, self.username)
        self.assertContains(response, "Username or password incorrect")

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
        username = "testuser"
        email = "testuser@test"
        password = "test"
        create_user_profile(username, email, password)
        self.client.login(username=username, password=password)
        url = reverse("logout")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, reverse("index"))
        self.assertNotContains(response, username)


class ConfirmViewTest(TestCase):
    """
    Collection of tests for RegisterConfirmView class.
    """

    username = "testuser"
    email = "testuser@test"
    password = "test"
    user_profile = None

    def setUp(self):
        self.user_profile = create_user_profile(
            self.username, self.email, self.password)
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

    def test_invalid_confiramtion_code(self):
        """
        Using invalid confirmation code should not activate inactive user.
        """
        url = reverse("register_confirm", args=(
            self.user_profile.id, get_random_string(32),))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.user_profile.user.refresh_from_db()
        self.assertFalse(self.user_profile.user.is_active)
