from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login.html', views.login, name="login"),
    path('name.html', views.get_name, name="name"),
]