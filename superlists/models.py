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
        help_text="associated to user by one-to-one relation"
    )

    def __str__(self):
        return str(self.creation_date) + ' ' + self.name

    def get_absolute_url(self):
        """Returns URL associated with ToDoList"""
        return reverse('list', kwargs={"todo_list_id": self.id})


class ToDoListItem(models.Model):
    """
    The ToDoListItem class represents one task on :model:`superlists.ToDoList`.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Name",
        help_text="user defined task name"
    )
    completed = models.BooleanField(
        default=False,
        verbose_name="Completed",
        help_text="determines whether the owner set a task as completed"
    )
    todo_list = models.ForeignKey(
        ToDoList,
        on_delete=models.CASCADE,
        verbose_name="To-Do list",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns URL associated with ToDoListItem"""
        return reverse('list', kwargs={"todo_list_id": self.todo_list.id})
