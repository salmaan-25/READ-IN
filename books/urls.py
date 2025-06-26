from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.search_books, name='search_books'),
    path('read/<int:book_id>/', views.read_book, name='read_book'),
    path('save/<int:book_id>/', views.save_book, name='save_book'),
    path('mybooks/', views.my_books, name='my_books'),

]

