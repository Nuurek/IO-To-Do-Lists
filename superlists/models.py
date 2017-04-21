from django.db import models


class ToDoList(models.Model):
    """
    The ToDoList class defines the main storage unit in application.

    Attributes:
        name - name of the list defined by user
        creation_date - determines when the list was created
        is_private - does user allow for displaying his/her list on main page
    """
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(
        'date created', auto_now_add=True, blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.creation_date) + ' ' + self.name


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
