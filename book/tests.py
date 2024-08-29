from django.test import TestCase
from django.urls import reverse

from book.models import Book, BookReview
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))
        self.assertContains(response, 'No books found.')

    def test_book_list(self):
        book1 = Book.objects.create(title='title1', description='description1', isbn='11111')
        book2 = Book.objects.create(title='title2', description='description2', isbn='22222')
        book3 = Book.objects.create(title='title3', description='description3', isbn='33333')

        response = self.client.get(reverse('books:list'))

        books = Book.objects.all()

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse('books:list')+"?page=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title='title1', description='description1', isbn='11111')
        response = self.client.get(reverse('books:detail', kwargs={'id':book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_page(self):
        book1 = Book.objects.create(title='title1', description='description1', isbn='11111')
        book2 = Book.objects.create(title='title2', description='description2', isbn='22222')
        book3 = Book.objects.create(title='title3', description='description3', isbn='33333')

        response = self.client.get(reverse("books:list") + "?q=title1")

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)


class BookReviewTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='kitob', description='kitob haqida', isbn='1234567')
        self.user = CustomUser.objects.create(
            username='abduqodir',
            first_name='abduqodirbek',
            last_name='dusmurodov',
            email='hackinge33@gmail.com'
        )
        self.user.set_password('kiber4224')
        self.user.save()

        self.client.login(username='abduqodir', password='kiber4224')

    def test_add_review(self):
        response = self.client.post(
            reverse('books:review', kwargs={'id':self.book.id}),
            data = {
                'starts_given': 3,
                'comment': 'this is comment'
            }
        )
        reviews = self.book.bookreview_set.all()
        self.assertEquals(reviews.count(), 1)
        self.assertEquals(reviews[0].starts_given, 3)
        self.assertEquals(reviews[0].comment, 'this is comment')
        self.assertEquals(reviews[0].user, self.user)
        self.assertEquals(reviews[0].book, self.book)
        self.assertEquals(response.status_code, 302)

    def test_no_comment(self):
        response = self.client.get(reverse('books:detail', kwargs={'id':self.book.id}))

        self.assertNotContains(response, 'Reviews')
        self.assertEquals(response.status_code, 200)

    def test_form_contain(self):
        response = self.client.post(
            reverse('books:review', kwargs={'id': self.book.id}),
            data={
                'starts_given': 6,
                'comment': 'this is comment'
            }
        )
        form = response.context['review_form']
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Ensure this value is less than or equal to 5.')
        self.assertFormError(form, 'starts_given', 'Ensure this value is less than or equal to 5.')


class EditReviewTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='kitob', description='kitob haqida', isbn='1234567')
        self.user = CustomUser.objects.create(
            username='abduqodir',
            first_name='abduqodirbek',
            last_name='dusmurodov',
            email='hackinge33@gmail.com'
        )
        self.user.set_password('kiber4224')
        self.user.save()
        self.review = BookReview.objects.create(
            user=self.user,
            book=self.book,
            comment="this is my comment",
            starts_given=5
        )

        self.client.login(username='abduqodir', password='kiber4224')

    def test_edit_review_get(self):
        response = self.client.get(reverse("books:edit-review",
                                           kwargs={'book_id':self.book.id, 'review_id':self.review.id}))
        self.assertContains(response, self.review.starts_given)
        self.assertContains(response, self.review.comment)

    def test_edit_review_post(self):
        response = self.client.post(
            reverse("books:edit-review", kwargs={'book_id': self.book.id, 'review_id': self.review.id}),
            data={
                "starts_given": 4,
                "comment": "this comment"
            }
        )
        review = BookReview.objects.all()
        self.assertEquals(review.count(), 1)
        self.assertEquals(review[0].starts_given, 4)
        self.assertEquals(review[0].comment, "this comment")
        self.assertEquals(response.status_code, 302)

    def test_confirm_delete(self):
        response = self.client.get(
            reverse("books:confirm-delete-review",
                    kwargs={'book_id':self.book.id, 'review_id':self.review.id}),
        )

        self.assertContains(response, self.book.title)
        self.assertContains(response, self.review.comment)
        self.assertEquals(response.status_code, 200)

    def test_delete_review(self):
        response = self.client.get(
            reverse("books:delete-review",
                    kwargs={'book_id': self.book.id, 'review_id': self.review.id}),
        )
        reviews = BookReview.objects.count()

        self.assertEquals(reviews, 0)
        self.assertEquals(response.status_code, 302)
