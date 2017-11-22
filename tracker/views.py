from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.formats import date_format
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import json

from .forms import SigninForm, SignupForm, TimeEntryForm, TimeEntryObjectiveForm
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
    return HttpResponseRedirect(reverse("tracker:dashboard"))


class SigninView(generic.FormView):
    template_name = "tracker/signin.html"
    form_class = SigninForm
    redirect_field_name = "next"

    def form_valid(self, form):
        username = form.cleaned_data.get("username_email")
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
        data["navbar_active"] = "signin"
        return data

    def get_success_url(self):
        return reverse("tracker:index")


class DashboardView(generic.TemplateView):
    template_name = "tracker/dashboard.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["navbar_active"] = "dashboard"
        new_entry = self.request.GET.get("new_entry")
        if new_entry is not None:
            data["new_entry"] = TimeEntry.objects.get(pk=new_entry)
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


class TimeEntryFormView(generic.CreateView):
    form_class = TimeEntryForm
    template_name = "tracker/entry.html"
    model = TimeEntry

    def form_valid(self, form):
        user = None
        submitter = None

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            submitter = form.cleaned_data.get("submitter")

        form.instance.user = user
        form.instance.submitter = submitter

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["navbar_active"] = "entry"
        return data

    def get_success_url(self):
        return reverse("tracker:dashboard") + "?new_entry={}".format(self.object.id)


class ObjectiveView(generic.DetailView):
    template_name = "tracker/objective.html"
    model = Objective
    pk_url_kwarg = "objective"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["form"] = TimeEntryObjectiveForm()
        return data


class TimeEntryObjectiveFormView(generic.FormView):
    template_name = "tracker/objective/time-entry-modal.html"
    form_class = TimeEntryObjectiveForm

    def form_valid(self, form):
        explanation = form.cleaned_data.get("explanation")
        effort = form.cleaned_data.get("effort")

        objective_id = self.kwargs["objective"]
        objective = Objective.objects.get(pk=objective_id)

        user = None
        submitter = None

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            submitter = form.cleaned_data.get("submitter")

        entry = TimeEntry(
            user=user,
            objective=objective,
            explanation=explanation,
            effort=effort,
            submitter=submitter
        )
        entry.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tracker:objective", kwargs={"objective": self.kwargs["objective"]})


def json_get_objectives(request):
    objective_list = Objective.objects.all().order_by("-date_created")
    json_list = []

    for objective in objective_list:
        json_list.append({
            "name": objective.name,
            "description": objective.description,
            "target": objective.target,
            "progression": objective.progression(),
            "date_created": date_format(objective.date_created, "F d, Y"),
        })

    return JsonResponse({"objectives": json_list})


@csrf_exempt
def json_create_entry(request):
    json_data = json.loads(request.body)

    explanation = json_data.get("explanation")
    objective = json_data.get("objective")
    submitter = json_data.get("submitter", "")
    effort = json_data.get("effort")

    entry = TimeEntry(
        user=None,
        objective_id=objective,
        explanation=explanation,
        effort=effort,
        submitter=submitter
    )
    entry.save()

    return HttpResponse(status=200)
