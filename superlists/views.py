from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import ToDoList
from .forms import ToDoListCreationForm

# Create your views here.


def index(request):
    latest_todo_lists = ToDoList.objects.order_by('-creation_date')[:10]
    template = loader.get_template('superlists/index.html')
    form = ToDoListCreationForm()
    context = {
        'latest_todo_lists': latest_todo_lists,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def detail(request, todo_list_id):
    todo_list = get_object_or_404(ToDoList, pk=todo_list_id)
    return render(request, 'superlists/detail.html', {'todo_list': todo_list})


def create_todo_list(request):
    if request.method == 'POST':
        form = ToDoListCreationForm(request.POST)
        if form.is_valid():
            todo_list = ToDoList.objects.create(
                name=form.cleaned_data['name'], is_private=form.cleaned_data['is_private'])
            todo_list.save()
            return HttpResponseRedirect('/' + str(todo_list.id) + '/')
