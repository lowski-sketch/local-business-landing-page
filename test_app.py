
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
            connection.execute("""
                CREATE TABLE provider_applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_name TEXT NOT NULL,
                    contact_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    business_address TEXT,
                    service_area TEXT NOT NULL,
                    services TEXT NOT NULL,
                    customer_types TEXT,
                    years_in_business TEXT,
                    insurance_info TEXT,
                    license_info TEXT,
                    website TEXT,
                    availability TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
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


    def valid_provider(self):
        return {
            "business_name": "Test Home Services",
            "contact_name": "Alex Provider",
            "email": "provider@example.com",
            "phone": "555-0200",
            "business_address": "123 Main Street",
            "service_area": "Berkeley, Elmhurst",
            "services": "Snow removal, lawn care",
            "customer_types": "Residential and commercial",
            "years_in_business": "5 years",
            "insurance_info": "General liability insurance",
            "license_info": "Will provide applicable licenses",
            "website": "https://example.com",
            "availability": "Weekdays and weekends",
	    "provider_agreement": "yes",
        }

    def test_valid_provider_application_is_saved_as_pending(self):
        response = self.client.post(
            "/api/providers",
            json=self.valid_provider(),
        )

        self.assertEqual(response.status_code, 201)
        result = response.get_json()
        self.assertEqual(result["status"], "pending")

        connection = sqlite3.connect(self.database_path)
        try:
            row = connection.execute("""
                SELECT business_name, email, service_area, status
                FROM provider_applications
                WHERE id = ?
            """, (result["id"],)).fetchone()
        finally:
            connection.close()

        self.assertEqual(
            row,
            (
                "Test Home Services",
                "provider@example.com",
                "Berkeley, Elmhurst",
                "pending",
            ),
        )

    def test_provider_application_missing_required_field_is_rejected(self):
        provider = self.valid_provider()
        provider["business_name"] = ""

        response = self.client.post(
            "/api/providers",
            json=provider,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.get_json()["error"])

    def test_provider_application_invalid_email_is_rejected(self):
        provider = self.valid_provider()
        provider["email"] = "not-an-email"

        response = self.client.post(
            "/api/providers",
            json=provider,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("valid email", response.get_json()["error"])

    def test_provider_application_non_json_request_is_rejected(self):
        response = self.client.post(
            "/api/providers",
            data="this is not JSON",
            content_type="text/plain",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("valid JSON", response.get_json()["error"])

    def test_provider_application_without_agreement_is_rejected(self):
        provider = self.valid_provider()
        provider.pop("provider_agreement")

        response = self.client.post(
            "/api/providers",
            json=provider,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("agree", response.get_json()["error"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
