from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.conf import settings


def index(request):
    title = "Bienvenue sur le serveur LitReview - cliquez sur l'application qui vous intéresse"
    context = {
        'message': title
    }
    return render(request, 'litapp/index.html', context)


def login_view(request):
    title = "Page de login"
    login_echec = ""

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            login_echec = "Nom d'utilisateur et/ou Mdp incorrect."

    context = {
        'message': title,
        'login_echec': login_echec,
    }
    return render(request, 'litapp/login.html', context)


def new_account(request):
    title = "Création d'un compte"
    context = {
        'message': title
    }
    return render(request, 'litapp/new_account.html', context)


def home_view(request):
    title = "Bienvenue à la maison"
    context = {
        'message': title
    }
    return render(request, 'litapp/home.html', context)
