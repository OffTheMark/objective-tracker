from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


def index(request):
    if request.user.is_authenticated():
        return render(request, "tracker/index.html")
    else:
        return render(request, "tracker/signin.html")


class SigninView(TemplateView):
    template_name = "tracker/signin.html"

    def get(self, request, *args, **kwargs):
        return render(request, "tracker/signin.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("tracker:index"))
        else:
            context = {"error": "No match was found for username/email and password."}
            return render(request, "tracker/signin.html", context)


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("tracker:index"))


class SignupView(TemplateView):
    template_name = "tracker/"

    def get(self, request, *args, **kwargs):
        return render(request, "tracker/signup.html")

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        error = None

        if password != confirm_password:
            error = "Passwords don't match."
        elif User.objects.filter(username=username).exists():
            error = "A user with this username already exists."
        elif User.objects.filter(email=email).exists():
            error = "A user with this email already exists."

        if error is not None:
            context = {"error": error}
            return render(request, "tracker/signup.html", context)
        else:
            user = User.objects.create_user(username, email=email, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("tracker:index"))

