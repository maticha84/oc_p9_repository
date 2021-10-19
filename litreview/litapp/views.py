from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from itertools import chain
from django.db.models.fields import CharField
from django.db.models import Value, Q
from django.contrib import messages

from .models import User, Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm


def index(request):
    """
    Diplay the page of the root server path
    """
    title = "Bienvenue sur le serveur LitReview - cliquez sur l'application qui vous intéresse"
    context = {
        'title_page': title
    }
    return render(request, 'litapp/index.html', context)


def login_view(request):
    """
    Display login page
    if request method is POST, connexion test
    """
    title = "Page de login"

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "Nom d'utilisateur et/ou Mdp incorrect.")

    context = {
        'title_page': title,
    }
    return render(request, 'litapp/login.html', context)


def logout_view(request):
    """
    logout view
    """
    messages.info(request, "Déconnexion effectuée. Veuillez vous reconnecter pour accéder au site.")
    logout(request)
    return redirect('login')


def new_account(request):
    """
    diplay creation user page
    if request method is POST, testing creation new user
    """
    title = "Création d'un compte"

    if request.POST:
        username = request.POST.get('new_username')
        user_test = User.objects.filter(username=username)
        if user_test:
            messages.error(request, "Le nom de l'utilisateur existe déjà. Veuillez réessayer")
            return redirect('new_account')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            validate_password(password1)
        except:
            messages.error(request, "Le mot de passe doit être complexe et contenir au moins 9 caractères")
            return redirect('new_account')

        if password1 != password2:
            messages.error(request, "Les mots de passe fournit ne correspondent pas")
            return redirect('new_account')

        user = User.objects.create_user(username=username, password=password1)
        messages.info(request, f"Création du compte {user.username} effectuée. Vous pouvez à présent vous connecter.")

    context = {
        'title_page': title,
    }
    return render(request, 'litapp/new_account.html', context)


@login_required(login_url='login')
def profile_view(request):
    title_page = "Profile"

    if request.POST:
        username = request.user.username
        user_modify = User.objects.get(username=username)

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            validate_password(password1)
        except:
            messages.error(request, "Le mot de passe doit être complexe et contenir au moins 9 caractères")

            return redirect('profile')

        if password1 != password2:
            messages.error(request, "Les mots de passe fournit ne correspondent pas")

            return redirect('profile')
        else:
            user_modify.set_password(password1)
            user_modify.save()
            messages.info(request, "Mot de passe modifié avec succès")
    context = {
        'title_page': title_page,
    }
    return render(request, 'litapp/profile.html', context)


@login_required(login_url='login')
def home_view(request):
    """
    Diplay flux page. It's the default page when user is login
    """
    title_page = "Flux"

    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {
        'title_page': title_page,
        'posts': posts,
    }

    return render(request, 'litapp/home.html', context)


def get_users_viewable_tickets(user):
    """
    get tickets from user and the users whose followed by user
    return : QuerySet of Ticket
    """
    users = UserFollows.objects.filter(user=user)
    user_follow = User.objects.filter(followed_by__in=users)

    tickets = Ticket.objects.filter(Q(user__in=user_follow) | Q(user=user))
    return tickets


def get_users_viewable_reviews(user):
    """
    get review from user and the users whose followed by user
    if a user not followed by the login user comment a ticket write by the user connected, it will be
    display to.
    return : QuerySet of Review
    """
    users = UserFollows.objects.filter(user=user)
    user_follow = User.objects.filter(followed_by__in=users)

    reviews = Review.objects.filter(
        Q(user__in=user_follow) |
        Q(ticket__user=user) |
        Q(ticket__user__in=user_follow) |
        Q(user=user)
    )
    return reviews


@login_required(login_url='login')
def review_create(request):
    """
    Display review without ticket creation
    Method post :
    first, creation of Ticket
    second : if Ticket is create, creation of Review
    """
    title_page = "Créer une critique"
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.title = ticket_form.cleaned_data['title']
            ticket.description = ticket_form.cleaned_data['description']
            ticket.image = ticket_form.cleaned_data['image']

            ticket.save()
        else:
            messages.error(request, "Le formulaire n'est pas valide.")
            return redirect('review')

        # On traite la critique que si le ticket a été enregistré précédemment
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.rating = review_form.cleaned_data['rating']
            review.headline = review_form.cleaned_data['headline']
            review.body = review_form.cleaned_data['body']

            review.save()
            return redirect('posts')

    context = {
        'title_page': title_page,
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'litapp/review.html', context)


@login_required(login_url='login')
def review_response(request, ticket_id):
    """
    Display review creation with existing ticket
    Method post : response of Ticket
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    title_page = f"Vous répondez au ticket {ticket.title}"

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.rating = review_form.cleaned_data['rating']
            review.headline = review_form.cleaned_data['headline']
            review.body = review_form.cleaned_data['body']
            review.save()
            return redirect('posts')
    else:
        review_form = ReviewForm()

    context = {
        'title_page': title_page,
        'review_form': review_form,
        'ticket': ticket,
    }

    return render(request, 'litapp/review_response.html', context)


@login_required(login_url='login')
def review_change(request, review_id):
    """
    Display modification review view
    """
    review = get_object_or_404(Review, pk=review_id)
    review_form = ReviewForm(instance=review)
    title_page = f"Vous modifiez la critique {review.id}"

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review.rating = review_form.cleaned_data['rating']
            review.headline = review_form.cleaned_data['headline']
            review.body = review_form.cleaned_data['body']
            review.save()
            return redirect('posts')

    context = {
        'title_page': title_page,
        'review_form': review_form,
        'ticket': review.ticket,
    }

    return render(request, 'litapp/review_response.html', context)


@login_required(login_url='login')
def review_delete(request, review_id):
    """
    Delete a review
    """
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('posts')


@login_required(login_url='login')
def ticket_create(request):
    """
    Display creation Ticket view
    """
    title_page = "Créer un ticket"
    ticket_form = TicketForm()

    if request.method == 'POST':

        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.title = ticket_form.cleaned_data['title']
            ticket.description = ticket_form.cleaned_data['description']
            ticket.image = ticket_form.cleaned_data['image']

            ticket.save()
            return redirect('posts')

    context = {
        'title_page': title_page,
        'ticket_form': ticket_form,
    }
    return render(request, 'litapp/ticket.html', context)


@login_required(login_url='login')
def ticket_change(request, ticket_id):
    """
    Diplay modification Ticket view
    """
    title_page = f"Modification du ticket {ticket_id}"
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket_form = TicketForm(instance=ticket)

    if request.method == 'POST':

        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket.title = ticket_form.cleaned_data['title']
            ticket.description = ticket_form.cleaned_data['description']
            if ticket_form.cleaned_data['image']:
                ticket.image = ticket_form.cleaned_data['image']

            ticket.save()
            return redirect('posts')

    context = {
        'title_page': title_page,
        'ticket_form': ticket_form,
        'ticket': ticket
    }
    return render(request, 'litapp/ticket.html', context)


@login_required(login_url='login')
def ticket_delete(request, ticket_id):
    """
    Delete Ticket
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('posts')


@login_required(login_url='login')
def posts_view(request):
    """
    Display Posts by time_created from the user
    """
    title_page = "Vos posts"
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {
        'title_page': title_page,
        'posts': posts,
    }

    return render(request, 'litapp/posts.html', context)


@login_required(login_url='login')
def follow_view(request):
    """
    Diplay follow view
    method POST : if username is valid and not followed by the user, add the following user
    """
    page_title = 'Abonnements'

    followed_by = UserFollows.objects.filter(user=request.user)
    following = UserFollows.objects.filter(followed_user=request.user)

    if request.method == 'POST':
        follow_user = request.POST.get('follow_user')
        if follow_user == request.user.username:
            messages.error(request, "Vous ne pouvez pas vous abonner à vous-même")
            return redirect('follow')

        existing_user = User.objects.filter(username=follow_user)

        if existing_user:
            existing_user = User.objects.get(username=follow_user)
            try:
                user_follows = UserFollows(user=request.user, followed_user=existing_user)
                user_follows.save()
                messages.info(request, f"Vous êtes abonnés à {existing_user.username}")
            except:
                messages.error(request, "Vous êtes déjà abonnés à cet utilisateur")
                return redirect('follow')
        else:
            messages.error(request, "Le nom de l'utilisateur demandé n'existe pas")
            return redirect('follow')

    context = {
        'title_page': page_title,
        'followed_by': followed_by,
        'following': following,
    }
    return render(request, 'litapp/follow.html', context)


@login_required(login_url='login')
def follow_delete(request, followed_by_id, following_id):
    """
    Delete following.
    """
    followed_by = UserFollows.objects.filter(user_id=following_id, followed_user_id=followed_by_id)
    if followed_by:
        followed_by = UserFollows.objects.get(user_id=following_id, followed_user_id=followed_by_id)
        followed_by.delete()
    return redirect('follow')
