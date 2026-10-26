
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app as localpro_app


class LocalProAPITests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test_leads.db"

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("""
                CREATE TABLE quote_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    service TEXT NOT NULL,
                    details TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
        finally:
            connection.close()

        self.database_patch = patch.object(
            localpro_app, "DATABASE", self.database_path
        )
        self.database_patch.start()

        self.addCleanup(self.database_patch.stop)
        self.addCleanup(self.temp_dir.cleanup)

        localpro_app.app.config["TESTING"] = True
        self.client = localpro_app.app.test_client()

    def valid_quote(self):
        return {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "555-0100",
            "service": "Home Services",
            "details": "Please contact me about a quote.",
        }

    def test_home_route(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("running", response.get_json()["message"])

    def test_valid_quote_is_saved(self):
        response = self.client.post(
            "/api/quotes",
            json=self.valid_quote(),
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

        connection = sqlite3.connect(self.database_path)
        try:
            row = connection.execute("""
                SELECT name, email, service
                FROM quote_requests
                WHERE id = ?
            """, (response.get_json()["id"],)).fetchone()
        finally:
            connection.close()

        self.assertEqual(
            row,
            ("Test Customer", "customer@example.com", "Home Services"),
        )

    def test_missing_required_field_is_rejected(self):
        quote = self.valid_quote()
        quote["name"] = ""

        response = self.client.post("/api/quotes", json=quote)

        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.get_json()["error"])

    def test_invalid_email_is_rejected(self):
        quote = self.valid_quote()
        quote["email"] = "not-an-email"

        response = self.client.post("/api/quotes", json=quote)

        self.assertEqual(response.status_code, 400)
        self.assertIn("valid email", response.get_json()["error"])

    def test_non_json_request_is_rejected(self):
        response = self.client.post(
            "/api/quotes",
            data="this is not JSON",
            content_type="text/plain",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("valid JSON", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
