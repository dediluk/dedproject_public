from django.shortcuts import render
from django.db.models import Sum
from django.views.generic.detail import DetailView
from .models import *


def aboutMe(request):
    return render(request, 'catalog/aboutMe.html')


def index(request):
    context = Book.objects.all()
    sum = Book.objects.aggregate(Sum('pages'))
    print(sum['pages__sum'])
    return render(request, 'catalog/index.html', {'context': context, 'sum':sum['pages__sum']})


class BookDetail(DetailView):
    model = Book
    template_name = 'catalog/bookDetail.html'
