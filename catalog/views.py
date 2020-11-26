from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Sum, Q
from django.views.generic import FormView, ListView, CreateView
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


def about_user(request, username):
    print('IN==========================')
    user = User.objects.get(Q(username=username.title()) | Q(username=username.lower()))
    return render(request, 'catalog/about_user.html', {'user': user})


# class MyBookslist(ListView):
#     model = MyBooksList
#     template_name = 'catalog/mybookslist.html'
#     print('===================================')
#     print(MyBooksList.objects.get(user=User.objects.get(username='admin')))
#     print('===================================')
#     # print(MyBooksList.objects.filter(user=User.objects.get(username='admin')))
#     # def get_queryset(self):
#     #     pass
# return MyBooksList.objects.filter(user=self.request.user)

def myBooksList(request):
    if request.user.is_anonymous:
        list = 'Войдите, что увидеть список своих книг.'
    else:
        list = MyBooksList.objects.filter(user=request.user)

    return render(request, 'catalog/mybookslist.html', {'list': list})

#
# class MyBooksListCreate(CreateView):
#     model = MyBooksList
#     fields = ['book']
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.user = self.request.user
#         obj.save()
#         return HttpResponseRedirect(self.get_success_url())
