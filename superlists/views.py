from django.views.generic import CreateView, ListView, TemplateView, FormView
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from .models import ToDoList, ToDoListItem, UserProfile
from .forms import ToDoListItemForm, UserForm


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


class RegisterView(FormView):
    form_class = UserForm
    template_name = 'superlists/register.html'
    model = User

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        user.is_active = False
        user.save()
        user_profile = UserProfile(
            user=user, confirmation_code=get_random_string(32))
        user_profile.save()
        #user_profile.send_confirmation_code()
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse("register_success")


class RegisterSuccessView(TemplateView):
    template_name = "superlists/register_success.html"


class RegisterConfirmView(TemplateView):
    template_name = "superlists/register_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile_id = kwargs["user_profile_id"]
        confirmation_code = kwargs["code"]
        user_profile = UserProfile.objects.get(id=user_profile_id)
        if user_profile.confirmation_code == confirmation_code:
            user_profile.activate_user()
            context["success"] = True
            context["username"] = user_profile.username
        else:
            context["success"] = False
        return context

