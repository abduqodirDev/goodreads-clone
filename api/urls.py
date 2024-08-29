from django.urls import path

# from api.views import BookReviewDetailAPIView, BookListAPIView
from rest_framework.routers import DefaultRouter
from api.views import BookReviewViewSet

router = DefaultRouter()
router.register("reviews", BookReviewViewSet, basename="review")


app_name = 'api'
urlpatterns = [
    # path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name='review-detail'),
    # path('reviews/', BookListAPIView.as_view(), name='review-list'),
]

urlpatterns += router.urls
