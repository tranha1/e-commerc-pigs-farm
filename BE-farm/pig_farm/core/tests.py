from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .apis import medicines


class MedicinesApiTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def _mock_cursor(self):
        mock_cursor = MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.__exit__.return_value = False
        mock_cursor.description = []
        mock_cursor.fetchall.return_value = []
        return mock_cursor

    @patch("pig_farm.core.apis.connection")
    def test_page_less_than_one_returns_400(self, mock_connection):
        request = self.factory.get("/medicines/", {"page": "0"})
        response = medicines(request)

        self.assertEqual(response.status_code, 400)
        mock_connection.cursor.assert_not_called()

    @patch("pig_farm.core.apis.connection")
    def test_page_size_less_than_one_returns_400(self, mock_connection):
        request = self.factory.get("/medicines/", {"page_size": "0"})
        response = medicines(request)

        self.assertEqual(response.status_code, 400)
        mock_connection.cursor.assert_not_called()

    @patch("pig_farm.core.apis.connection")
    def test_non_integer_values_default_to_safe_numbers(self, mock_connection):
        mock_cursor = self._mock_cursor()
        mock_connection.cursor.return_value = mock_cursor

        request = self.factory.get("/medicines/", {"page": "abc", "page_size": "xyz"})
        response = medicines(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["page"], 1)
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM v_medicine_public ORDER BY published_at DESC, id DESC LIMIT %s OFFSET %s",
            [20, 0],
        )
