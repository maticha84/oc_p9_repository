from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('new_account/', views.new_account, name="new_account"),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('ticket/', views.ticket_create, name='ticket_create'),
    path('posts/', views.posts_view, name='posts'),
    path('review/', views.review_create, name='review_create'),
    path('<int:ticket_id>/review_response/', views.review_response, name='review_response'),
    path('<int:review_id>/review_change/', views.review_change, name='review_change'),
    path('<int:ticket_id>/ticket_change/', views.ticket_change, name='ticket_change'),
    path('<int:review_id>/review_delete/', views.review_delete, name='review_delete'),
    path('<int:ticket_id>/ticket_delete/', views.ticket_delete, name='ticket_delete'),
]
