from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from itertools import chain
from django.db.models.fields import CharField
from django.db.models import Value

from .models import User, Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm


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
    success = ""

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

        success = f"Création du compte {user.username} effectuée. Vous pouvez à présent vous connecter."
    context = {
        'message': title,
        'success': success,
    }

    return render(request, 'litapp/new_account.html', context)


@login_required(login_url='/litapp/login.html')
def home_view(request):
    title_page = "Bienvenue à la maison"
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')

    #reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    #tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {
        'message': title_page,
        'tickets': tickets,
        'reviews': reviews,
        'posts': posts,
    }

    return render(request, 'litapp/home.html', context)


@login_required(login_url='/litapp/login.html')
def review_create(request):
    title_page = "Créer une critique"

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        if ticket_form.is_valid():
            title = ticket_form.cleaned_data['title']
            description = ticket_form.cleaned_data['description']
            image = ticket_form.cleaned_data['image']

            ticket.save()
        else:
            ticket_form = TicketForm()
            review_form = ReviewForm()

            context = {
                'message': title_page,
                'review_form': review_form,
                'ticket_form': ticket_form,
            }
            return render(request, 'litapp/review.html', context)

        # On traite la critique que si le ticket a été enregistré précédemment
        review_form = ReviewForm(request.POST, request.FILES)
        review = review_form.save(commit=False)
        review.user = request.user
        review.ticket = ticket
        if review_form.is_valid():
            rating = review_form.cleaned_data['rating']
            headline = review_form.cleaned_data['headline']
            body = review_form.cleaned_data['body']

            review.save()
            return HttpResponseRedirect('posts.html')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        'message': title_page,
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'litapp/review.html', context)


@login_required(login_url='/litapp/login.html')
def review_response(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    title_page = f"Vous répondez au ticket {ticket.title}"

    if request.method == 'POST':
        # On traite la critique que si le ticket a été enregistré précédemment
        review_form = ReviewForm(request.POST, request.FILES)
        review = review_form.save(commit=False)
        review.user = request.user
        review.ticket = ticket
        if review_form.is_valid():
            rating = review_form.cleaned_data['rating']
            headline = review_form.cleaned_data['headline']
            body = review_form.cleaned_data['body']
            review.save()
            return HttpResponseRedirect('/litapp/posts.html')
    else:
        review_form = ReviewForm()

    context = {
        'message': title_page,
        'review_form': review_form,
        'ticket': ticket,
    }

    return render(request, 'litapp/review_response.html', context)


@login_required(login_url='/litapp/login.html')
def ticket_create(request):
    title_page = "Créer un ticket"

    if request.method == 'POST':

        ticket_form = TicketForm(request.POST, request.FILES)
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        if ticket_form.is_valid():
            title = ticket_form.cleaned_data['title']
            description = ticket_form.cleaned_data['description']
            image = ticket_form.cleaned_data['image']
            context = {
                'message': title_page,
                'ticket_form': ticket_form,
            }

            ticket.save()
            return HttpResponseRedirect('posts.html')
    else:
        ticket_form = TicketForm()
    context = {
        'message': title_page,
        'ticket_form': ticket_form,
    }
    return render(request, 'litapp/ticket.html', context)


@login_required(login_url='/litapp/login.html')
def ticket_change(request, ticket_id):
    title_page = f"Modification du ticket {ticket_id}"
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket_data = {
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'image': ticket.image,
        'user': ticket.user,
        'time_created': ticket.time_created
    }
    if request.method == 'POST':

        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket.title = ticket_form.cleaned_data['title']
            ticket.description = ticket_form.cleaned_data['description']
            if ticket_form.cleaned_data['image']:
                ticket.image = ticket_form.cleaned_data['image']

            ticket.save()
            return HttpResponseRedirect('/litapp/posts.html')
    else:
        ticket_form = TicketForm(ticket_data)

    context = {
        'message': title_page,
        'ticket_form': ticket_form,
        'ticket': ticket
    }
    return render(request, 'litapp/ticket.html', context)


@login_required(login_url='/litapp/login.html')
def posts_view(request):
    title_page = "Vos posts"
    tickets = Ticket.objects.order_by('-time_created')
    reviews = Review.objects.order_by('-time_created')

    # reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    # tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {
        'message': title_page,
        'tickets': tickets,
        'reviews': reviews,
        'posts': posts,
    }

    return render(request, 'litapp/posts.html', context)
