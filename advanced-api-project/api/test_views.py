from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="tester",
            password="password123"
        )

        self.client = APIClient()
        self.client.login(username="tester", password="password123")

        # Endpoints
        self.book_list_url = reverse("book-list")
        self.book_create_url = reverse("book-create")

        # Create initial book
        self.book = Book.objects.create(
            title="First Book",
            author="Author One",
            publication_year=2020
        )

    # -------------------------------
    # TEST: List Books
    # -------------------------------
    def test_list_books(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    # -------------------------------
    # TEST: Create Book
    # -------------------------------
    def test_create_book(self):
        payload = {
            "title": "New Book",
            "author": "Someone",
            "publication_year": 2023
        }
        response = self.client.post(self.book_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    # -------------------------------
    # TEST: Retrieve a Single Book
    # -------------------------------
    def test_get_single_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "First Book")

    # -------------------------------
    # TEST: Update Book (PUT)
    # -------------------------------
    def test_update_book(self):
        url = reverse("book-update", kwargs={"pk": self.book.id})
        payload = {
            "title": "Updated Book",
            "author": "New Author",
            "publication_year": 2024
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    # -------------------------------
    # TEST: Delete Book
    # -------------------------------
    def test_delete_book(self):
        url = reverse("book-delete", kwargs={"pk": self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    # -------------------------------
    # TEST: Filtering
    # -------------------------------
    def test_filter_books(self):
        response = self.client.get(self.book_list_url + "?author=Author One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["author"], "Author One")

    # -------------------------------
    # TEST: Searching
    # -------------------------------
    def test_search_books(self):
        response = self.client.get(self.book_list_url + "?search=First")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "First Book")

    # -------------------------------
    # TEST: Ordering
    # -------------------------------
    def test_order_books(self):
        response = self.client.get(self.book_list_url + "?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure ordered list
        self.assertTrue(isinstance(response.data, list))
