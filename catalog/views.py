from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage

from .forms import *
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, CreateView
from django.views.generic.detail import DetailView
from .models import *


def about_me(request):
    return render(request, 'catalog/about_me.html')


class RegisterFormView(FormView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        # print(User.objects.get(username=form.cleaned_data['username']))
        # user = User.objects.get(username=form.cleaned_data['username'])
        # print(user)
        # user.is_active = False
        # email_subject = 'Активация аккаунта'
        # email_body = 'TEST'
        # email = send_mail(
        #     email_subject,
        #     email_body,
        #     settings.EMAIL_HOST_USER,
        #     ['dediluk@gmail.com'],
        # )
        #
        # email.send(fail_silently=True)
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


# class PasswordChangeFormView(FormView):
#     form_class = PasswordChangeForm
#     success_url = reverse_lazy('catalog:index')
#     template_name = 'accounts/change-password.html'
#     use
#
#     def form_valid(self, form):
#         form.save()
#         return super(PasswordChangeForm, self).form_valid(form)
#
#     def form_invalid(self, form):
#         return super(PasswordChangeForm, self).form_invalid(form)

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('catalog:profile')
        else:
            return render(request, 'accounts/change-password.html', {'form': form})

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change-password.html', args)


def index(request):
    context = Book.objects.all()
    sum = Book.objects.aggregate(Sum('pages'))

    return render(request, 'catalog/index.html', {'context': context, 'sum': sum['pages__sum']})


def book_detail(request, slug):
    book = Book.objects.get(slug=slug)
    print(book.slug)
    marker = False
    if request.user.is_authenticated:
        bl = BookList.objects.filter(user=request.user)
        for i in bl:
            if i.book_list == book:
                marker = True
                break
    return render(request, 'catalog/book_detail.html', {'book': book, 'marker': marker})


@login_required
def add_book(request):
    form = CreateBookForm(request.POST, request.FILES or None)

    if form.is_valid():
        form.save()
        book = Book.objects.filter(title=form['title'].value()).order_by('book_add_user')[0]
        book.book_add_user = request.user
        book.save()
        return HttpResponseRedirect(reverse_lazy('catalog:index'))
    return render(request, 'catalog/add_book.html', {'form': form})


def profile(request, username=None):
    if username:
        user = User.objects.get(username=username)
    else:
        user = request.user
    return render(request, 'catalog/profile.html', {'user': user})


@user_passes_test(lambda u: u.is_superuser)
def delete_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
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
    bl = BookList.objects.filter(user=request.user)
    bl.get(book_list=book).delete()
    messages.info(request, 'The item was deleted to your wishlist')
    return redirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda u: u.is_superuser)
def edit_book_data(request, slug):
    book = Book.objects.get(slug=slug)
    form = CreateBookForm(initial={'title': book.title, 'pages': book.pages, 'image': book.image})
    if request.method == 'POST':
        form = CreateBookForm(request.POST, request.FILES or None)
        if form['title'].value():
            book.title = form['title'].value()
        if form['pages'].value():
            book.pages = form['pages'].value()
        if form['image'].value():
            book.image = form['image'].value()
        book.save()
        return HttpResponseRedirect(reverse_lazy('catalog:index'))
    else:
        return render(request, "catalog/edit_data.html", {"form": form})


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

    return render(request, 'catalog/my_books_list.html', {'list_of_mybook': list_of_mybook, 'sum_pages': sum_pages})


class SearchResult(ListView):
    model = Book
    template_name = 'catalog/search.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Book.objects.filter(Q(title__icontains=query.lower()) | Q(title__icontains=query.title()))
        return object_list
