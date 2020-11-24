from django.db import models


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
