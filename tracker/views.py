from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, ListView

from .forms import SigninForm, SignupForm
from .models import Objective


def get_user_by_email_or_username(username_email):
    try:
        user = User.objects.get(email=username_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(username=username_email)
        except User.DoesNotExist:
            user = None

    return user


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("tracker:dashboard/overview"))
    else:
        return HttpResponseRedirect(reverse("tracker:signin"))


class SigninView(FormView):
    template_name = "tracker/signin.html"
    form_class = SigninForm
    redirect_field_name = "next"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = get_user_by_email_or_username(username)

        if user is not None and user.check_password(password):
            login(self.request, user)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["navbar_active"] = "signin"
        return data

    def get_success_url(self):
        url = self.request.POST.get(self.redirect_field_name)
        if url is None:
            url = reverse("tracker:index")
        return url


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("tracker:index"))


class SignupView(FormView):
    template_name = "tracker/signup.html"
    form_class = SignupForm

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = User.objects.create_user(username, email=email, password=password)
        login(self.request, user)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["navbar_active"] = "signup"
        return data

    def get_success_url(self):
        return reverse("tracker:index")


class DashboardOverviewView(LoginRequiredMixin, ListView):
    template_name = "tracker/dashboard/overview.html"
    model = Objective

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["navbar_active"] = "dashboard"
        data["sidebar_active"] = "overview"
        return data

    def get_queryset(self):
        return Objective.objects.all()
