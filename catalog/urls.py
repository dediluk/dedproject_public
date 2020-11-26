from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *


app_name = 'catalog'

urlpatterns = [
    path('about', aboutMe, name='aboutMe'),
    path('', index, name='index'),
    path('<int:pk>/', BookDetail.as_view(), name='book_detail'),
    path('accounts/register/', RegisterFormView.as_view(), name='register'),
    path('about_user/<str:username>', about_user, name='about_user'),
    path('mybookslist/', myBooksList, name='mybookslist')
]
