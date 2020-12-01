from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField('Название', max_length=150)
    pages = models.IntegerField('Количество страниц')
    image = models.ImageField("Обложка", upload_to='images/books', blank=True)
    book_add_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Добавил', blank=True, null=True,
                                      on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    def Meta(self):
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    class Meta:
        ordering = ['title']


class BookList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_list = models.ForeignKey(Book, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.book_list.title
