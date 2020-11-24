from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import *


def aboutMe(request):
    return render(request, 'catalog/aboutMe.html')


def index(request):
    context = Book.objects.all()
    return render(request, 'catalog/index.html', {'context': context})


class BookDetail(DetailView):
    model = Book
    template_name = 'catalog/bookDetail.html'
