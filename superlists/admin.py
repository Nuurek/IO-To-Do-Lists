from django.contrib import admin

from .models import ToDoList, ToDoListItem


admin.site.register(ToDoList)
admin.site.register(ToDoListItem)
