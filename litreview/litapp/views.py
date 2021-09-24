from django.shortcuts import render


def index(request):
    message = "salut la foule"
    context = {
        'message': message
    }
    return render(request, 'litapp/index.html', context)
