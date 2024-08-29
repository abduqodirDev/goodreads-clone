from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from book.models import BookReview


def landing_page(request):
    return render(request, "landing.html")


def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(book_reviews, page_size)

    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)

    return render(request, "home.html", {"page_object":page_object})
