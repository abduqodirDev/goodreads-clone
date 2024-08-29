from django.test import TestCase
from django.urls import reverse

from book.models import BookReview, Book
from users.models import CustomUser


class HomeReviewTestCase(TestCase):
    def test_home_review(self):
        book = Book.objects.create(title='kitob', description='kitob haqida', isbn='1234567')
        user = CustomUser.objects.create(
            username='abduqodir',
            first_name='abduqodirbek',
            last_name='dusmurodov',
            email='hackinge33@gmail.com'
        )
        user.set_password('kiber4224')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, starts_given=4, comment="nice good boo1")
        review2 = BookReview.objects.create(book=book, user=user, starts_given=3, comment="nice good boo2")
        review3 = BookReview.objects.create(book=book, user=user, starts_given=5, comment="nice good boo3")

        response = self.client.get(reverse('home_page') + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
        self.assertEquals(response.status_code, 200)
