from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from .forms import SigninForm, SignupForm, TimeEntryForm
from .models import Objective, TimeEntry


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
        return HttpResponseRedirect(reverse("tracker:dashboard"))
    else:
        return HttpResponseRedirect(reverse("tracker:signin"))


class SigninView(generic.FormView):
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


class SignupView(generic.FormView):
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


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "tracker/dashboard.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["navbar_active"] = "dashboard"
        return data


def dashboard_objectives(request):
    if request.is_ajax():
        list = Objective.objects.all().order_by("-date_created")
        content = render_to_string("tracker/dashboard/objectives.html", {"objectives": list})
        return HttpResponse(content)


def dashboard_time_entries(request):
    if request.is_ajax():
        list = TimeEntry.objects.all().order_by("-date_created")[:20]
        content = render_to_string("tracker/dashboard/time-entries.html", {"time_entries": list})
        return HttpResponse(content)


class TimeEntryView(LoginRequiredMixin, generic.FormView):
    template_name = "tracker/entry.html"
    form_class = TimeEntryForm

    def form_valid(self, form):
        objective = form.cleaned_data.get("objective")
        explanation = form.cleaned_data.get("explanation")
        effort = form.cleaned_data.get("effort")

        entry = TimeEntry(
            user=self.request.user,
            objective=objective,
            explanation=explanation,
            effort=effort
        )
        entry.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["navbar_active"] = "entry"
        return data

    def get_success_url(self):
        return reverse("tracker:entry")
