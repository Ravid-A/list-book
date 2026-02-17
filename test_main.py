import unittest
from fastapi.testclient import TestClient
import main  # חשוב לייבא את המודול עצמו

client = TestClient(main.app)


class TestBooksAPI(unittest.TestCase):

    def setUp(self):
        # איפוס מלא לפני כל בדיקה
        main.books.clear()
        main.counter = 1

    def test_get_empty_books(self):
        response = client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_add_book(self):
        response = client.post(
            "/books",
            json={"title": "Clean Code", "author": "Robert C. Martin", "year": 1998}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], "Clean Code")
        self.assertEqual(data["author"], "Robert C. Martin")
        self.assertEqual(data["year"], 1998)

    def test_get_book_by_id(self):
        client.post(
            "/books",
            json={"title": "Test Book", "author": "Tester", "year": 1998}
        )

        response = client.get("/books/1")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["title"], "Test Book")
        self.assertEqual(data["author"], "Tester")
        self.assertEqual(data["year"], 1998)

    def test_delete_book(self):
        client.post(
            "/books",
            json={"title": "Delete Me", "author": "Author", "year": 1998}
        )

        response = client.delete("/books/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Book deleted")

    def test_get_non_existing_book(self):
        response = client.get("/books/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Book not found")


if __name__ == "__main__":
    unittest.main()
