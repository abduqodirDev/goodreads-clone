from rest_framework import serializers

from book.models import Book, BookReview
from users.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    book = BookSerializer(required=False)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ('id', 'starts_given', 'comment', 'user', 'book', 'user_id', 'book_id')

