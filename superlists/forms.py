from django import forms
from .models import ToDoList, ToDoListItem


class ToDoListCreationForm(forms.ModelForm):
    """
    Form for creating ToDoList objects.
    Allows rendering, parsing, sanitizing and saving objects to DB.
    """
    class Meta:
        model = ToDoList
        fields = '__all__'


class ToDoListItemForm(forms.ModelForm):

    class Meta:
        model = ToDoListItem
        fields = ("name",)


class ToDoListItemAdditionForm(forms.Form):
    """
    Form for creating ToDoListItem objects.
    Contains only one field: name.
    Allows rendering, parsing, sanitizing and saving objects to DB.
    """
    name = forms.CharField(label="", max_length=200)
