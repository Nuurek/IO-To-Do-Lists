from django.db import models
from django.utils import timezone

# Create your models here.


class ToDoList(models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(
        'date created', auto_now_add=True, blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.creation_date) + ' ' + self.name


class ToDoListItem(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
