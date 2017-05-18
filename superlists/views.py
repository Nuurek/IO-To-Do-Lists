from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView, FormView, DeleteView

from .forms import ToDoListItemForm
from .models import ToDoList, ToDoListItem, UserProfile


class ToDoListCreateView(CreateView):
    """
    View that allows to create new instances of ToDoList.
    """
    model = ToDoList
    fields = ("name", "is_private")

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            user = self.request.user
            form.instance.user_profile = UserProfile.objects.get(user=user)
        return super(ToDoListCreateView, self).form_valid(form)


class PublicToDoListListView(ListView):
    queryset = ToDoList.objects.all().filter(is_private__exact=False)
    fields = "__all__"
    context_object_name = "todo_lists"


class IndexMixin(ToDoListCreateView, PublicToDoListListView):
    """
    Display home page of SuperLists website.
    """
    template_name = "superlists/index.html"


class ToDoListDetailView(TemplateView):
    """
    Displays details of :model:`superlists.ToDoList`.

    **Context**

    ``todo_list``
        :model:`superlists.ToDoList`

    ``to_do_list_items``
        :model:`superlists.ToDoListItem`\s associated with this ToDoList
    """
    template_name = "superlists/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list_id = self.kwargs["todo_list_id"]
        todo_list = ToDoList.objects.get(id=todo_list_id)
        context["todo_list"] = todo_list
        context["to_do_list_items"] = ToDoListItem.objects.all().filter(
            todo_list=todo_list.pk)
        context["form"] = ToDoListItemForm()
        return context


class ToDoListItemCreateView(FormView):
    form_class = ToDoListItemForm

    def form_valid(self, form):
        form.instance.todo_list = ToDoList.objects.get(
            id=self.kwargs["todo_list_id"])
        form.save()
        result = super(ToDoListItemCreateView, self).form_valid(form)
        return result

    def get_success_url(self):
        todo_list_id = self.kwargs["todo_list_id"]
        return reverse("list", kwargs={"todo_list_id": todo_list_id})


class ToDoListItemDeleteView(TemplateView):

    def get(self, request, todo_list_id, todo_list_item_id):
        try:
            ToDoList.objects.get(id=todo_list_id)
        except ToDoList.DoesNotExist:
            raise Http404("List does not exist")
        try:
            todo_list_item = ToDoListItem.objects.get(id=todo_list_item_id)
        except ToDoListItem.DoesNotExist:
            raise Http404("Task does not exist")
        if todo_list_item:
            todo_list_item.delete()
        return HttpResponseRedirect(reverse("list", kwargs={"todo_list_id": todo_list_id}))


class ToDoListDeleteView(DeleteView):
    template_name="superlists/delete_list.html"
    model = ToDoList

    def get_success_url(self):
        return reverse("index")
