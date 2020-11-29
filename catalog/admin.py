from django.contrib import admin
from .models import *

class BookListAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_list')

admin.site.register(Book)
admin.site.register(BookList, BookListAdmin)
