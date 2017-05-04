from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import ToDoList, ToDoListItem


def create_todo_list(name, is_private):
    """
    Create new ToDoList at present time and add it to database.

    Attributes:
        name - name of the list
        private - should list be displayed on main page
    """
    return ToDoList.objects.create(name=name, creation_date=timezone.now(), is_private=is_private)


def create_todo_list_item(name, completed, todo_list):
    """
    Create new ToDo List Item for given ToDo List.

    Attributes:
        name - name of the item
        completed - whether item is completed
        todo_list - ToDo List to which item belongs
    """
    return ToDoListItem.objects.create(name=name, completed=completed, todo_list=todo_list)


class IndexViewTests(TestCase):

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
