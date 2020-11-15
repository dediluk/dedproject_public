from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'catalog'

urlpatterns = [
    path('about', aboutMe, name='aboutMe'),
    path('', index, name='index')
]
