from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, CreateView
from django.views.generic.detail import DetailView
from .models import *


def aboutMe(request):
    return render(request, 'catalog/aboutMe.html')


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    # "/accounts/registration/?next=/mybookslist/"
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

    return render(request, 'catalog/index.html', {'context': context, 'sum': sum['pages__sum']})


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    bl = BookList.objects.filter(user=request.user)
    marker = False
    for i in bl:
        if i.book_list == book:
            marker = True
            break
    return render(request, 'catalog/bookDetail.html', {'book': book, 'marker':marker})


# class BookDetail(DetailView):
#     model = Book
#     template_name = 'catalog/bookDetail.html'


def about_user(request, username):
    user = User.objects.get(Q(username=username.title()) | Q(username=username.lower()))
    return render(request, 'catalog/about_user.html', {'user': user})


@login_required
def add_to_booklist(request, title):
    item = get_object_or_404(Book, title=title)

    wished_item, created = BookList.objects.get_or_create(book_list=item,
                                                          slug=item.title,
                                                          user=request.user,
                                                          )

    messages.info(request, 'The item was added to your wishlist')
    return redirect('catalog:index')

@login_required
def delete_from_booklist(request, title):
    book = Book.objects.get(title=title)
    bl = BookList.objects.filter(user=request.user)
    bl.get(book_list=book).delete()
    messages.info(request, 'The item was deleted to your wishlist')
    return redirect('catalog:index')

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
    if request.user.is_anonymous or not request.user.is_authenticated:
        list_of_mybook = 'Войдите, что увидеть список своих книг.'
        sum_pages = 0
    elif request.user.is_authenticated:
        list_of_mybook = BookList.objects.filter(user=request.user)

        sum_pages = 0
        for i in list_of_mybook:
            print(dir(i))
            sum_pages += i.book_list.pages

    return render(request, 'catalog/mybookslist.html', {'list_of_mybook': list_of_mybook, 'sum_pages': sum_pages})

# def add_to_booklist(request, pk):
#     print('hi')
#     print('=============================')
#     book = Book.objects.get(pk=pk)
#     user = request.user
#     print(book, user)
#     MyBooksList.book = book
#     MyBooksList.user = user
#     MyBooksList.save()
#     return HttpResponseRedirect(reverse_lazy('catalog:index'))
# class MyBooksListCreate(CreateView):
#     model = MyBooksList
#     fields = ['book']
#     print(1)
#
#     def form_valid(self, form):
#         print(2)
#         obj = form.save(commit=False)
#         print(3)
#         obj.user = self.request.user
#         print(4)
#         obj.save()
#         print(5)
#         return HttpResponseRedirect(reverse_lazy('catalog:index'))
