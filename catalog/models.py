from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField('Название', max_length=150)
    pages = models.IntegerField('Количество страниц')
    image = models.ImageField("Обложка", upload_to='images/books')

    def __str__(self):
        return self.title

    def Meta(self):
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    class Meta:
        ordering = ['title']


class MyBooksList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING, related_name='userslist')
    book = models.ForeignKey(Book,
                             on_delete=models.DO_NOTHING, related_name='bookslist')

    class Meta:
        unique_together = ['user', 'book']
