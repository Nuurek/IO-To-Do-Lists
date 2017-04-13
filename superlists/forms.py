from django import forms
from .models import ToDoList

'''
Form for creating ToDoList objects.
Allows rendering, parsing, sanitizing and saving objects to DB.
'''
class ToDoListCreationForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = '__all__'


'''
Form for creating ToDoListItem objects.
Contains only one field: name.
Allows rendering, parsing, sanitizing and saving objects to DB.
'''
class ToDoListItemAdditionForm(forms.Form):
    name = forms.CharField(label="", max_length=200)
