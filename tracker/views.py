from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from .forms import SigninForm, SignupForm


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
    if request.user.is_authenticated():
        return render(request, "tracker/index.html")
    else:
        return HttpResponseRedirect(reverse("tracker:signin"))


class SigninView(TemplateView):
    template_name = "tracker/signin.html"

    def get(self, request, *args, **kwargs):
        form = SigninForm()

        return render(request, "tracker/signin.html", {"form": form})

    def post(self, request):
        form = SigninForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = get_user_by_email_or_username(username)

            if user is not None and user.check_password(password):
                login(request, user)
                return HttpResponseRedirect(reverse("tracker:index"))

        return render(request, "tracker/signin.html", {"form": form})


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("tracker:index"))


class SignupView(TemplateView):
    template_name = "tracker/signup.html"

    def get(self, request, *args, **kwargs):
        form = SignupForm

        return render(request, "tracker/signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = User.objects.create_user(username, email=email, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("tracker:index"))

        return render(request, "tracker/signup.html", {"form": form})

