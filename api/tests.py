from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from book.models import Book, BookReview
from users.models import CustomUser


class BookReviewApiTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='abduqodir', first_name='abduqodir1')
        self.user.set_password('kiber4224')
        self.user.save()
        self.book = Book.objects.create(title='kitob', description='kitob haqida', isbn='1234567')

        self.client.login(username='abduqodir', password='kiber4224')

    def test_review_detail(self):
        review = BookReview.objects.create(user=self.user, book=self.book, starts_given=5, comment='this is comment')
        response = self.client.get(reverse('api:review-detail', kwargs={'id':review.id}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['id'], review.id)
        self.assertEquals(response.data['starts_given'], 5)
        self.assertEquals(response.data['comment'], 'this is comment')
        self.assertEquals(response.data['user']['username'], 'abduqodir')
        self.assertEquals(response.data['user']['id'], review.user.id)
        self.assertEquals(response.data['user']['first_name'], 'abduqodir1')
        self.assertEquals(response.data['user']['last_name'], '')
        self.assertEquals(response.data['user']['email'], '')
        self.assertEquals(response.data['book']['id'], review.book.id)
        self.assertEquals(response.data['book']['title'], 'kitob')
        self.assertEquals(response.data['book']['description'], 'kitob haqida')
        self.assertEquals(response.data['book']['isbn'], '1234567')

    def test_review_list(self):
        BookReview.objects.create(user=self.user, book=self.book, starts_given=4, comment='this is comment1')
        BookReview.objects.create(user=self.user, book=self.book, starts_given=5, comment='this is comment2')
        response = self.client.get(reverse('api:review-list'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data['results']), 2)
        self.assertEquals(len(response.data), 4)
        self.assertEquals(response.data['results'][0]['starts_given'], 5)
        self.assertEquals(response.data['results'][0]['comment'], 'this is comment2')
        self.assertEquals(response.data['results'][1]['starts_given'], 4)
        self.assertEquals(response.data['results'][1]['comment'], 'this is comment1')

    def test_delete_review(self):
        review = BookReview.objects.create(starts_given=5, comment="this is comment", user=self.user, book=self.book)
        response = self.client.delete(reverse("api:review-detail", kwargs={'id':review.id}))

        reviews = BookReview.objects.count()
        self.assertEquals(response.status_code, 204)
        self.assertEquals(reviews, 0)

    def test_patch_review(self):
        review = BookReview.objects.create(starts_given=5, comment="this is comment", user=self.user, book=self.book)
        response = self.client.patch(reverse('api:review-detail',
                                             kwargs={'id':review.id}),
                                             data={"starts_given":1}
                                     )
        review.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(review.starts_given, 1)

    def test_put_review(self):
        review = BookReview.objects.create(starts_given=5, comment="this is comment", user=self.user, book=self.book)
        response = self.client.patch(reverse('api:review-detail',
                                             kwargs={'id': review.id}),
                                     data={
                                         "starts_given": 1,
                                         "comment": "comment",
                                         "user": self.user,
                                         "book": self.book
                                     }
                                     )

        review.refresh_from_db()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(review.starts_given, 1)
        self.assertEquals(review.comment, "comment")
        self.assertEquals(review.user, self.user)
        self.assertEquals(review.book, self.book)

    def test_create_review(self):
        response = self.client.post(reverse("api:review-list"), data={
            "starts_given": 1,
            "comment": "this is comment",
            "user_id": self.user.id,
            "book_id": self.book.id
        })

        reviews = BookReview.objects.count()
        review = BookReview.objects.all()[0]
        self.assertEquals(response.status_code, 201)
        self.assertEquals(reviews, 1)
        self.assertEquals(review.starts_given, 1)
        self.assertEquals(review.user, self.user)
        self.assertEquals(review.book, self.book)
        self.assertEquals(review.comment, "this is comment")

