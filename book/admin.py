from django.contrib import admin

from .models import Book, Author, BookAuthor, BookReview


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'description')
    search_fields = ('title', 'isbn')
    inlines = (BookAuthorInline, )


class AuthorAdmin(admin.ModelAdmin):
    pass


class BookAuthorAdmin(admin.ModelAdmin):
    pass


class BookReviewAdmin(admin.ModelAdmin):
    pass



admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
