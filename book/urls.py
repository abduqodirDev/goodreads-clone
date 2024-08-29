from django.urls import path

from book.views import BookView, BookDetailView, AddReviewView, EditReviewView, ConfirmDeleteReviewView,\
DeleteReviewView

app_name='books'
urlpatterns = [
    path('', BookView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/review/', AddReviewView.as_view(), name='review'),
    path('<int:book_id>/review/<int:review_id>/edit/', EditReviewView.as_view(), name='edit-review'),
    path(
        '<int:book_id>/review/<int:review_id>/delete/confirm/',
        ConfirmDeleteReviewView.as_view(),
        name='confirm-delete-review'
    ),
    path('<int:book_id>/review/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete-review'),
]
