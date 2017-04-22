from django.http import HttpResponseRedirect, Http404
from django.views.generic import CreateView, ListView, TemplateView, FormView
from django.urls import reverse
from django.shortcuts import redirect

from .models import ToDoList, ToDoListItem
from .forms import ToDoListCreationForm, ToDoListItemForm


class ToDoListCreateView(CreateView):
    model = ToDoList
    fields = "__all__"


class PublicToDoListListView(ListView):
    queryset = ToDoList.objects.all().filter(is_private__exact=False)
    fields = "__all__"
    context_object_name = "todo_lists"


class IndexMixin(ToDoListCreateView, PublicToDoListListView):
    template_name = "superlists/index.html"


class ToDoListDetailView(TemplateView):
    template_name = "superlists/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list_id = self.kwargs["todo_list_id"]
        todo_list = ToDoList.objects.get(id=todo_list_id)
        context["todo_list"] = todo_list
        context["to_do_list_items"] = ToDoListItem.objects.all().filter(todo_list=todo_list.pk)
        context["form"] = ToDoListItemForm()
        return context

    model = ToDoList
    fields = "__all__"


class ToDoListItemCreateView(FormView):
    form_class = ToDoListItemForm

    def form_valid(self, form):
        form.instance.todo_list = ToDoList.objects.get(id=self.kwargs["todo_list_id"])
        return super(ToDoListItemCreateView, self).form_valid(form)

    def get_success_url(self):
        id = self.kwargs["todo_list_id"]
        return redirect("list", todo_list_id=id)


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
            return HttpResponseRedirect(reverse("list", kwargs={"todo_list_id": todo_list.id}))
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
