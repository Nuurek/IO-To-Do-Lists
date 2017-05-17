from django.db import models
from django.urls import reverse

from accounts.models import UserProfile


class ToDoList(models.Model):
    """
    The ToDoList class defines the main storage unit in application.

    Attributes:
        name - name of the list defined by user
        creation_date - determines when the list was created
        is_private - does user allow for displaying his/her list on main page
        user_profile - profile of the user this list belongs to, can be null
    """
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(
        'date created', auto_now_add=True, blank=True)
    is_private = models.BooleanField(default=False)
    user_profile = models.ForeignKey(
        UserProfile, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.creation_date) + ' ' + self.name

    def get_absolute_url(self):
        return reverse('list', kwargs={"todo_list_id": self.id})


class ToDoListItem(models.Model):
    """
    Represents a single task on a todo list.

    Attributes:
        name - title of the item
        completed - true if task is marked as completed, false otherwise
        todo_list - ToDoList corresponding to this item
    """
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list', kwargs={"todo_list_id": self.todo_list.id})
