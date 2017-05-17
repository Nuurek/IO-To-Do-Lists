from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, FormView

from superlists.models import ToDoList
from .forms import UserForm
from .models import UserProfile


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
