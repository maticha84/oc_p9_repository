from django.shortcuts import render


# Create your views here.

def index(request):
    message = "salut la foule"
    context = {
        'message': message
    }
    return render(request, 'LITReview_app/index.html', context)
