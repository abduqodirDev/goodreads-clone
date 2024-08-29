from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from book.forms import BookReviewForm
from book.models import Book, BookReview


class BookView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'books': page_obj,
            'search_query': search_query
        }
        return render(request, 'book/list.html', context)


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        context = {
            'book': book,
            'review_form': review_form
        }
        return render(request, 'book/detail.html', context)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                starts_given=review_form.cleaned_data.get('starts_given'),
                comment=review_form.cleaned_data.get('comment')
            )

            return redirect(reverse('books:detail', kwargs={'id':book.id}))

        context = {
            'book': book,
            'review_form': review_form
        }
        return render(request, 'book/detail.html', context)


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        context = {
            'book': book,
            'review': review,
            'review_form': review_form
        }
        return render(request, "book/edit_review.html", context)

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)
        if review_form.is_valid():
            review_form.save()

            return redirect("books:detail", id=book.id)

        context = {
            'book': book,
            'review': review,
            'review_form': review_form
        }
        return render(request, "book/edit_review.html", context)


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id,  *args, **kwargs):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        return render(request, "book/confirm_delete_review.html", {'book':book, 'review':review})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "you have successfully delated this review.")
        return redirect('books:detail', id=book.id)
