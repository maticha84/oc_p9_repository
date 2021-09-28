from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password

from .models import User

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


def new_account(request):
    title = "Création d'un compte"
    echec = ""

    if request.POST:
        username = request.POST.get('new_username')
        user_test = User.objects.filter(username=username)
        if user_test:
            echec = "Le nom de l'utilisateur existe déjà. Veuillez réessayer"
            context = {
                'message': title,
                'echec': echec,
            }

            return render(request, 'litapp/new_account.html', context)

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            validate_password(password1)
        except:
            echec = "Le mot de passe doit être complexe et contenir au moins 9 caractères"
            context = {
                'message': title,
                'echec': echec,
            }
            return render(request, 'litapp/new_account.html', context)
        if password1 != password2:
            echec = "Les mots de passe fournit ne correspondent pas"
            context = {
                'message': title,
                'echec': echec,
            }
            return render(request, 'litapp/new_account.html', context)

        user = User.objects.create_user(username=username, password=password1)
        echec = f"Création du compte {user.username} effectuée. Vous pouvez à présent vous connecter."
    context = {
        'message': title,
        'echec': echec,
    }

    return render(request, 'litapp/new_account.html', context)


@login_required(login_url='/litapp/')
def home_view(request):
    title = "Bienvenue à la maison"
    context = {
        'message': title
    }

    return render(request, 'litapp/home.html', context)
