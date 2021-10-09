from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login.html', views.login_view, name='login'),
    path('new_account.html', views.new_account, name="new_account"),
    path('home.html', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('ticket.html', views.ticket_create, name='ticket_create'),
    path('posts.html', views.posts_view, name='posts'),
    path('review.html', views.review_create, name='review_create'),
    re_path(r'(?P<ticket_id>[0-9]+)/review_response.html', views.review_response, name='review_response'),
    re_path(r'(?P<ticket_id>[0-9]+)/ticket_change.html', views.ticket_change, name='ticket_change'),
]
