from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm
# Create your views here.

def index(request):
    message = "salut la foule"
    context = {
        'message': message
    }
    return render(request, 'LITReview_app/index.html', context)


def login(request):
    message = "page de login"
    context = {
        'message': message
    }
    return render(request, 'LITReview_app/login.html', context)


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        context = {'form': form}
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'LITReview_app/thanks.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        context = {'form': form}
    return render(request, 'LITReview_app/name.html', context)
