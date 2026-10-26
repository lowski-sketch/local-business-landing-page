# LocalPro - Local Business Landing Page

LocalPro is a responsive landing-page project designed for local service businesses. It provides a professional web presence and a quote-request form connected to a Python backend.

## Live Demo

[View the LocalPro website](https://glistening-youtiao-ef3f15.netlify.app/)

**Deployment note:** The public Netlify site currently hosts the frontend. The Flask backend runs locally on the developer's computer, so the public site is not yet connected to a publicly hosted quote-processing service.

## Features

- Responsive layout for desktop and mobile
- Professional navy, white, and green design
- Service cards and business benefits
- Quote-request form with browser-side validation
- JavaScript form submission using the Fetch API
- Flask API for receiving quote requests
- SQLite storage for submitted quote information
- Success and error messages
- Automatic footer year

## Technologies

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- Flask-CORS
- SQLite
- Git

## How It Works

1. A visitor fills out the quote-request form.
2. JavaScript sends the form data to the Flask API.
3. The backend processes the request and stores it in SQLite.
4. The page displays a success or error message.

The local form-to-database workflow has been tested successfully.

## Run Locally

Requirements: Python and a terminal. Git is optional.

1. Open a terminal in the project folder.
2. Create a virtual environment if needed:

   ```bat
   python -m venv .venv
   ```

3. Activate the environment on Windows:

   ```bat
   .venv\Scripts\activate
   ```

4. Install the dependencies:

   ```bat
   python -m pip install Flask Flask-CORS
   ```

5. Start the backend:

   ```bat
   python app.py
   ```

6. Open `index.html` in a browser and test the quote form.

The frontend currently sends requests to `http://127.0.0.1:5000/api/quotes`. The backend must be running on the same computer. Other visitors cannot use your computer's local address through the public Netlify website.

## Data and Privacy

Quote submissions are stored in a local SQLite database named `leads.db`. The database is excluded from Git to help prevent local submission data from being committed to the repository.

This is a development prototype, not yet a production-ready lead-management system. Before using it with real customers, add suitable security and privacy controls, server-side validation, production hosting, HTTPS, and a connection between the public frontend and deployed backend.

## Future Improvements

- Deploy the Flask backend publicly
- Connect the Netlify frontend to the deployed API
- Configure production CORS rules
- Add stronger server-side validation and spam protection
- Improve accessibility and browser testing
- Add business-specific branding and contact information

## Automated Tests

The project includes five automated tests for the Flask API:

- Confirms the home route responds successfully.
- Verifies valid quote requests are saved to the SQLite database.
- Rejects requests with missing required fields.
- Rejects invalid email addresses.
- Rejects requests that do not contain valid JSON.

Run the tests from the project folder with:

```powershell
.venv\Scripts\python.exe -m unittest -v test_app.py
```

The tests use a temporary database, keeping test submissions separate from the local project database.

## Skills Demonstrated

- Building a responsive web interface
- Connecting JavaScript forms to a Python API
- Processing HTTP requests with Flask
- Persisting submitted data in SQLite
- Troubleshooting cross-origin requests (CORS)
- Testing a local form-to-database workflow
- Tracking changes with Git
- Documenting software setup and limitations
