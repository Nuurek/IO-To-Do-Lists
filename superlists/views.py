from django.views.generic import CreateView, ListView, TemplateView, FormView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator

from .models import ToDoList, ToDoListItem, UserProfile
from .forms import ToDoListItemForm, UserForm


class ToDoListCreateView(CreateView):
    model = ToDoList
    fields = ("name","is_private")

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

class ToDoListItemDeleteView(TemplateView):

    def get(self, request, todo_list_id, todo_list_item_id):
        todo_list = ToDoList.objects.get(id=todo_list_id)
        todo_list_item = ToDoListItem.objects.get(id=todo_list_item_id)
        if todo_list_item:
            todo_list_item.delete()
        return HttpResponseRedirect(reverse("list", kwargs={"todo_list_id": todo_list_id}))

class RegisterView(FormView):
    EMAIL_VERIFICATON = True

    form_class = UserForm
    template_name = 'superlists/register.html'
    model = User

    def form_valid(self, form):
        user = form.save()
        print(user.password)
        user.set_password(user.password)
        if self.EMAIL_VERIFICATON:
            user.is_active = False
        user.save()
        user_profile = UserProfile(
            user=user, confirmation_code=get_random_string(32))
        user_profile.save()
        if self.EMAIL_VERIFICATON:
            user_profile.send_confirmation_code()
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
            context["username"] = user_profile.user.username
        else:
            context["success"] = False
        return context


class UserProfileView(ListView):
    template_name = "superlists/user.html"
    fields = "__all__"
    context_object_name = "todo_lists"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user_id=self.request.user.id)
        return ToDoList.objects.all().filter(user_profile=user_profile)


class ToDoListDeleteView(DeleteView):
    template_name="superlists/delete_list.html"
    model = ToDoList

    def get_success_url(self):
        return reverse("index")


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
            else:
                messages.add_message(
                    request, messages.WARNING, 'This account is not active')
        else:
            messages.add_message(request, messages.WARNING,
                                 'Username or password incorrect')
        return HttpResponseRedirect(reverse("index"))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
