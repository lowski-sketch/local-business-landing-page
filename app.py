
from flask_cors import CORS
from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path
import re

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "leads.db"


def initialize_database():
    """Create the quote-request table if it does not exist."""
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS quote_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                service TEXT NOT NULL,
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "LocalPro Python backend is running."
    })


@app.route("/api/quotes", methods=["POST"])
def create_quote():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a valid JSON request."
        }), 400

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    service = str(data.get("service", "")).strip()
    details = str(data.get("details", "")).strip()

    if not name or not email or not service:
        return jsonify({
            "error": "Name, email, and service are required."
        }), 400

    if len(name) > 100 or len(email) > 254:
        return jsonify({
            "error": "Name or email is too long."
        }), 400

    if len(phone) > 40 or len(service) > 100 or len(details) > 3000:
        return jsonify({
            "error": "One or more fields exceed the allowed length."
        }), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({
            "error": "Please enter a valid email address."
        }), 400

    connection = sqlite3.connect(DATABASE)
    try:
        cursor = connection.execute("""
            INSERT INTO quote_requests
                (name, email, phone, service, details)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, service, details))

        quote_id = cursor.lastrowid
        connection.commit()
    finally:
        connection.close()

    return jsonify({
        "message": "Your quote request was received.",
        "id": quote_id
    }), 201


if __name__ == "__main__":
    initialize_database()
    app.run(host="127.0.0.1", port=5000, debug=False)
