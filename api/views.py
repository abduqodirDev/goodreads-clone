from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from book.models import BookReview, Book
from api.serializers import BookReviewSerializer, BookSerializer


class BookReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-id')
    lookup_field = 'id'



# class BookReviewDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(book_review).data
#
#         return Response(serializer)
#
#     def delete(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         book_review.delete()
#
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def put(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         book_review = BookReview.objects.get(id=id)
#         serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class BookListAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         book_reviews = BookReview.objects.all().order_by('-id')
#
#         paginate = PageNumberPagination()
#         page_obj = paginate.paginate_queryset(book_reviews, request)
#
#         serializer = BookReviewSerializer(page_obj, many=True).data
#
#         return paginate.get_paginated_response(serializer)
#
#     def post(self, request):
#         serializer = BookReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
