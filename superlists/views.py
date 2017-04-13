from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse

from .models import ToDoList, ToDoListItem
from .forms import ToDoListCreationForm, ToDoListItemAdditionForm


def index(request):
    """
    Handles HTTP request for the main page.

    Args:
        request - HTTP request

    Returns:
        HTTP response with the main page view.
    """

    latest_todo_lists = ToDoList.objects.order_by('-creation_date')[:10]
    template = loader.get_template('superlists/index.html')
    form = ToDoListCreationForm()
    context = {
        'latest_todo_lists': latest_todo_lists,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def detail(request, todo_list_id):
    """
    Handles HTTP request for the detailed view of a list.

    Args:
        request - HTTP request
        todo_list_id - id of a list to display

    Returns:
        HTTP response with list details view if list exists, 404 error code page otherwise.
    """
    todo_list = get_object_or_404(ToDoList, pk=todo_list_id)
    template = loader.get_template('superlists/detail.html')
    form = ToDoListItemAdditionForm()
    context = {
        'todo_list': todo_list,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def create_todo_list(request):
    """
    Handles HTTP request to create new list.
    If POST creates new list according to user input.
    Args:
        request - HTTP request

    Returns:
        Redirect to detailed view of newly created list if POST, 404 error code page otherwise.
    """
    if request.method == 'POST':
        form = ToDoListCreationForm(request.POST)
        if form.is_valid():
            todo_list = form.save()
            return HttpResponseRedirect(reverse("detail", kwargs={"todo_list_id": todo_list.id}))
    else:
        raise Http404("Resource does not exist")

def add_todo_list_item(request, todo_list_id):
    """
    Handles HTTP request to create new item in a list.
    If POST creates new item on a list according to user input.
    Args:
        request - HTTP request
        todo_list_id - id of a list corresponding to the new item

    Returns:
        Redirect to detailed view of corresponding list if POST, 404 error code page otherwise.
    """
    if request.method == 'POST':
        form = ToDoListCreationForm(request.POST)
        if form.is_valid():
            todo_list = ToDoList.objects.get(pk=todo_list_id)
            todo_list_item = ToDoListItem(name=form.cleaned_data['name'], todo_list=todo_list)
            todo_list_item.save()
            return HttpResponseRedirect('/' + str(todo_list_id) + '/')
    else:
        raise Http404("Resource does not exist")
