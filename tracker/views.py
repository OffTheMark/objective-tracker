from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


def index(request):
    if request.user.is_authenticated():
        return render(request, "tracker/index.html")
    else:
        return render(request, "tracker/signin.html")


def signin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
    return HttpResponseRedirect("/tracker")


def signout(request):
    logout(request)
    return HttpResponseRedirect("/tracker")
