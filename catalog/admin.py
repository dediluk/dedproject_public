from django.contrib import admin
from .models import *


class BookListAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_list')


class BookAddUserAdmin(admin.ModelAdmin):
    list_display = ('title', 'book_add_user')


admin.site.register(Book, BookAddUserAdmin)
admin.site.register(BookList, BookListAdmin)
