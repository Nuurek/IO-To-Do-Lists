from django import forms
from .models import ToDoListItem


class ToDoListItemForm(forms.ModelForm):

    class Meta:
        model = ToDoListItem
        fields = ("name",)