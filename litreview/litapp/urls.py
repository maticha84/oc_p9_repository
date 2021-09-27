from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('new_account.html', views.new_account, name="new_account"),
    path('home.html', views.home_view, name='home'),
]
