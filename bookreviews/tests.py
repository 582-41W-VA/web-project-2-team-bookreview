from django.test import TestCase
from django.urls import reverse


class CheckAllPages(TestCase):

    # testing homepage and make sure is working
    def test_index_page(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    # testing single book detail page
    def test_book_detail_page(self):
        # response with correct book id from api
        response = self.client.get(
            reverse("book_detail", kwargs={"book_id": "oMoYDAAAQBAJ"})
        )
        self.assertEqual(response.status_code, 200)

        # response if given wrong book id
        error_response = self.client.get(
            reverse("book_detail", kwargs={"book_id": "1"})
        )
        self.assertEqual(error_response.status_code, 404)

    def test_register_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "firstname": "test",
                "lastname": "user",
                "password": "1234",
            },
        )

        self.assertEqual(response.status_code, 200)
