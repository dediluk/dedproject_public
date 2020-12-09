from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify
from random import randrange

User._meta.get_field('email')._unique = True


class Book(models.Model):
    title = models.CharField('Название', max_length=150)
    pages = models.IntegerField('Количество страниц')
    # image = models.ImageField("Обложка", upload_to='images/books', blank=True)
    image = models.CharField("Ссылка на обложку",  blank=True, max_length=250)
    book_add_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Добавил', blank=True, null=True,
                                      on_delete=models.DO_NOTHING)
    slug = models.SlugField(null=True, blank=True, default=None, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + str(randrange(1000))
        super(Book, self).save(*args, **kwargs)

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

# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
