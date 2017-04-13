from django import forms
from .models import ToDoList


class ToDoListCreationForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = '__all__'

class ToDoListItemAdditionForm(forms.Form):
    name = forms.CharField(label="", max_length=200)
