from django.db import models
from django.urls import reverse

from accounts.models import UserProfile


class ToDoList(models.Model):
    """
    The ToDoList class defines the main storage unit in the application.
    Associates many :model:`superlists.ToDoListItem`.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Name of the to-do list",
        help_text="defined by user"
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name="Creation date",
        help_text="saved on the first time the list was created"
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name="Private",
        help_text="determines whether list was created by user or not"
    )
    user_profile = models.ForeignKey(
        UserProfile,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Profile",
        help_text="associated to user by one-to-one relation"
    )

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
