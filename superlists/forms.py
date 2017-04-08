from django import forms


class ToDoListCreationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    is_private = forms.BooleanField(label="Private", required=False)

class ToDoListItemAdditionForm(forms.Form):
    name = forms.CharField(label="", max_length=200)
