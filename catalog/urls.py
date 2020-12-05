from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'catalog'

urlpatterns = [
    # Books
    path('mybookslist/', my_books_list, name='mybookslist'),
    path('add_to_booklist/<str:title>', add_to_booklist, name='add_to_booklist'),
    path('delete_from_booklist/<str:title>', delete_from_booklist, name='delete_from_booklist'),
    path('book_details/<int:pk>/', book_detail, name='book_detail'),
    path('add_book/', add_book, name='add_book'),
    path('mybookslist/', my_books_list, name='mybookslist'),
    path('add_to_booklist/<str:title>', add_to_booklist, name='add_to_booklist'),
    path('delete_from_booklist/<str:title>', delete_from_booklist, name='delete_from_booklist'),
    path('delete_book/<int:pk>', delete_book, name='delete_book'),
    path('edit_book_data/<int:pk>', edit_book_data, name='edit_book_data'),

    # Site
    path('about', about_me, name='aboutMe'),
    path('', index, name='index'),
    path('search/', SearchResult.as_view(), name='search'),

    # Accounts
    path('accounts/register/', RegisterFormView.as_view(), name='register'),
    path(r'profile/<str:username>', profile, name='profile'),
    path(r'profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
    path('accounts/password_reset', auth_view.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_view. , name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_confirm'),
    # path('password_reset/complete', auth_view.password_reset_complete, name='password_reset_complete'),

]
