from django.contrib import admin
from .models import ToDoList, ToDoListItem
# Register your models here.

admin.site.register(ToDoList)
admin.site.register(ToDoListItem)