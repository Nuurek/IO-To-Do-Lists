from django.views.generic import CreateView, ListView, TemplateView, FormView
from django.urls import reverse

from .models import ToDoList, ToDoListItem
from .forms import ToDoListItemForm


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


class ToDoListItemCreateView(FormView):
    form_class = ToDoListItemForm

    def form_valid(self, form):
        form.instance.todo_list = ToDoList.objects.get(id=self.kwargs["todo_list_id"])
        form.save()
        result = super(ToDoListItemCreateView, self).form_valid(form)
        return result

    def get_success_url(self):
        todo_list_id = self.kwargs["todo_list_id"]
        return reverse("list", kwargs={"todo_list_id": todo_list_id})
