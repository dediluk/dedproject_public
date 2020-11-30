from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, CreateView
from django.views.generic.detail import DetailView
from .models import *


def about_me(request):
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
        return super(RegisterFormView, self).form_invalid(form)


def index(request):
    context = Book.objects.all()
    sum = Book.objects.aggregate(Sum('pages'))

    return render(request, 'catalog/index.html', {'context': context, 'sum': sum['pages__sum']})


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    marker = False
    print(request.META.get('HTTP_REFERER'))
    if request.user.is_authenticated:
        bl = BookList.objects.filter(user=request.user)
        for i in bl:
            if i.book_list == book:
                marker = True
                break
    return render(request, 'catalog/bookDetail.html', {'book': book, 'marker': marker})


# class BookDetail(DetailView):
#     model = Book
#     template_name = 'catalog/bookDetail.html'


@login_required
def add_book(request):
    form = CreateBookForm(request.POST, request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('catalog:index'))
    return render(request, 'catalog/add_book.html', {'form': form})


def about_user(request, username):
    user = User.objects.get(Q(username=username.title()) | Q(username=username.lower()))
    return render(request, 'catalog/about_user.html', {'user': user})


@user_passes_test(lambda u: u.is_superuser)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    get_book = Book.objects.all()
    return HttpResponseRedirect(reverse("catalog:index"))


@login_required
def add_to_booklist(request, title):
    item = get_object_or_404(Book, title=title)

    wished_item, created = BookList.objects.get_or_create(book_list=item,
                                                          slug=item.title,
                                                          user=request.user,
                                                          )

    messages.info(request, 'The item was added to your wishlist')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_from_booklist(request, title):
    book = Book.objects.get(title=title)
    print(request.META.get('HTTP_REFERER'))
    bl = BookList.objects.filter(user=request.user)
    bl.get(book_list=book).delete()
    messages.info(request, 'The item was deleted to your wishlist')
    return redirect(request.META.get('HTTP_REFERER'))


# if form.cleaned_data['title']:
#     book.title = form.cleaned_data['title']
# if form.cleaned_data['pages']:
#     book.pages = form.cleaned_data['pages']
# if form.cleaned_data['image']:
#     book.image = form.cleaned_data['image']
# book.save()


def edit_data(request, pk):

    book = Book.objects.get(pk=pk)
    form = CreateBookForm(initial={'title': book.title, 'pages': book.pages, 'image': book.image})
    if request.method == 'POST':

        form = CreateBookForm(request.POST, request.FILES or None)
        print(form['title'].value())
        if form['title'].value():
            book.title = form['title'].value()
        if form['pages'].value():
            book.pages = form['pages'].value()
        if form['image'].value():
            book.image = form['image'].value()
        book.save()
        # if form.is_valid():
        #     book.title = form.cleaned_data['title']
        #     book.pages = form.cleaned_data['pages']
        #     book.image = form.cleaned_data['image']
        #     book.save()
        #
        #     return HttpResponseRedirect(reverse_lazy('catalog:index'))
        return HttpResponseRedirect(reverse_lazy('catalog:index'))
    else:
        return render(request, "catalog/edit_data.html", {"form": form})
#         book.title = request.POST.get('title')
#         book.pages = request.POST.get('pages')
#         print('============================')
#         print(request.FILES.get('image'))
#         if request.POST.get('image'):
#             book.image = request.FILES.get('image')
#         book.save()
#         return render(request, 'catalog/bookDetail.html', {'book':book})
#     else:
#         return render(request, "catalog/edit_data.html", {"book": book})
# except Book.DoesNotExist:
#     return HttpResponseNotFound("<h2>Person not found</h2>")
    # try:
    #
    #     if request.method == 'POST':
    #         book.title = request.POST.get('title')
    #         book.pages = request.POST.get('pages')
    #         print('============================')
    #         print(request.FILES.get('image'))
    #         if request.POST.get('image'):
    #             book.image = request.FILES.get('image')
    #         book.save()
    #         return render(request, 'catalog/bookDetail.html', {'book':book})
    #     else:
    #         return render(request, "catalog/edit_data.html", {"book": book})
    # except Book.DoesNotExist:
    #     return HttpResponseNotFound("<h2>Person not found</h2>")



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

@login_required
def my_books_list(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        list_of_mybook = 'Войдите, что увидеть список своих книг.'
        sum_pages = 0
    elif request.user.is_authenticated:
        list_of_mybook = BookList.objects.filter(user=request.user)

        sum_pages = 0
        for i in list_of_mybook:
            sum_pages += i.book_list.pages

    return render(request, 'catalog/mybookslist.html', {'list_of_mybook': list_of_mybook, 'sum_pages': sum_pages})


class SearchResult(ListView):
    model = Book
    template_name = 'catalog/search.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Book.objects.filter(Q(title__icontains=query.lower()) | Q(title__icontains=query.title()))
        print(object_list)
        return object_list

# def search(request):
#     search = request.search
#     book = Book.objects.get(title__contains=search)
#     print(book)
#     if book:
#         return render(request, 'catalog/search.html', {'book':book})
#     return render(request, 'catalog/search.html', {'book': book})

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
