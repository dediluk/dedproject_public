from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from .models import *


def aboutMe(request):
    return render(request, 'catalog/aboutMe.html')


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/accounts/registration/?next=/mybooks"
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        print('=====================================')
        return super(RegisterFormView, self).form_invalid(form)


def index(request):
    context = Book.objects.all()
    sum = Book.objects.aggregate(Sum('pages'))
    print(sum['pages__sum'])
    return render(request, 'catalog/index.html', {'context': context, 'sum': sum['pages__sum']})


class BookDetail(DetailView):
    model = Book
    template_name = 'catalog/bookDetail.html'
