from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.urls import reverse


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


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("tracker:index"))
