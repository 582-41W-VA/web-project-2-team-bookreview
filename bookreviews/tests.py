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

    # testing for registering new user
    def test_register_user(self):
        # response if register success
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "firstname": "test",
                "lastname": "user",
                "password1": "Bintang1234",
                "password2": "Bintang1234",
            },
        )
        # if success it will return 302 because it will redirect to login page
        self.assertEqual(response.status_code, 302)

        # response if register failed because of missing field
        error_response = self.client.post(
            reverse("register"),
            {
                "email": "testuser@email.com",
                "firstname": "test",
                "lastname": "user",
                "password": "1234",
            },
        )
        # it return 200 because will rerender register page again
        self.assertEqual(error_response.status_code, 200)
