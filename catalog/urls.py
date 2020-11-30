from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'catalog'

urlpatterns = [
    path('about', about_me, name='aboutMe'),
    path('', index, name='index'),
    path('book_details/<int:pk>/', book_detail, name='book_detail'),
    path('accounts/register/', RegisterFormView.as_view(), name='register'),
    path('about_user/<str:username>', about_user, name='about_user'),
    path('mybookslist/', my_books_list, name='mybookslist'),
    path('add_to_booklist/<str:title>', add_to_booklist, name='add_to_booklist'),
    path('delete_from_booklist/<str:title>', delete_from_booklist, name='delete_from_booklist'),
    path('search/', SearchResult.as_view(), name='search'),
    path('add_book/', add_book, name='add_book'),
    path('delete_book/<int:pk>', delete_book, name='delete_book')
]
