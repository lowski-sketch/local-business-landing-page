# LocalPro – Full-Stack Local Services Marketplace

**LocalPro** is a full-stack web application designed to connect customers with local service providers. The platform is being developed to simplify service requests, provider onboarding, and application management while creating a scalable foundation for a local services marketplace.

The project demonstrates practical full-stack development using Python, Flask, PostgreSQL, JavaScript, and cloud deployment services.

## Live Application

- **Website:** [https://localpro.lotpod.net](https://localpro.lotpod.net)
- **Provider Registration:** [https://localpro.lotpod.net/provider.html](https://localpro.lotpod.net/provider.html)
- **Administrator Dashboard:** [https://localpro.lotpod.net/admin.html](https://localpro.lotpod.net/admin.html)
- **Backend API:** [https://localpro-api.onrender.com](https://localpro-api.onrender.com)

The administrator dashboard requires authorized credentials.

## Project Overview

LocalPro is being developed around three primary workflows:

1. Customers submit requests for local services.
2. Service providers submit applications to join the platform.
3. Administrators review provider applications and approve or reject them.

The longer-term objective is to develop a reliable marketplace with provider management, qualified customer leads, and a sustainable business model.

## Features

### Customer Features
- Responsive customer-facing website.
- Service quote-request form.
- Browser-side form validation.
- JavaScript form submission using the Fetch API.
- Flask API integration.
- Database storage for customer requests.
- Email notifications for new quote submissions.
- Configured reply-to functionality for customer inquiries.

### Provider Features
- Dedicated provider registration page.
- Business and contact information collection.
- Service area and service category information.
- Business experience, insurance, and licensing information.
- Provider agreement validation.
- Database storage of provider applications.
- Pending application status upon submission.

### Administrator Features
- Password-protected administrator login.
- Authenticated API requests.
- Provider application management.
- Application approval and rejection.
- Provider status updates.
- Application refresh and logout functionality.

Additional dashboard enhancements, including application counts, search, status filters, and snow-service identification, are currently being tested locally before deployment.

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| API | REST API, JSON, Fetch API |
| Database | PostgreSQL, SQLite |
| Database connectivity | psycopg |
| Email | Resend |
| Hosting | Netlify, Render |
| Database hosting | Neon |
| Version control | Git, GitHub |
| Testing | Python unittest, Node.js assertions |

## Application Architecture

The application uses a separated frontend and backend architecture.

**Frontend**
- HTML, CSS, and JavaScript.
- Hosted through Netlify.
- Communicates with the backend through HTTP requests.

**Backend**
- Python and Flask.
- Hosted through Render.
- Processes customer requests and provider applications.
- Handles administrator authentication and provider status updates.

**Database**
- Neon PostgreSQL for the deployed application.
- SQLite fallback for local development and testing.

**Email**
- Resend integration for customer quote notifications.

## How the Application Works

### Customer Request Workflow

1. A customer visits the LocalPro website.
2. The customer completes the quote-request form.
3. JavaScript sends the information to the Flask API.
4. The backend validates and stores the request.
5. An email notification is sent through Resend.
6. The customer receives a submission confirmation.

### Provider Registration Workflow

1. A service provider visits the provider registration page.
2. The provider submits business and service information.
3. The backend validates required information and agreement acceptance.
4. The application is stored in the database.
5. The application receives a pending status.
6. An administrator reviews the application.
7. The administrator can approve or reject the application.

## Database Design

The application maintains separate records for customer quote requests and provider applications.

Provider application records include:
- Business name
- Contact information
- Business address
- Service area
- Services offered
- Customer types
- Years in business
- Insurance information
- Licensing information
- Website
- Availability
- Application status
- Submission timestamp

Database configuration supports PostgreSQL in the deployed environment and SQLite for local development.

## Automated Testing

The backend includes automated unit tests using Python's `unittest` framework.

The test suite covers:
- API route behavior.
- Valid customer submissions.
- Required field validation.
- Invalid email rejection.
- Invalid JSON handling.
- Provider application validation.
- Provider agreement requirements.
- Administrator authentication and provider status operations.

**Backend test suite:** 18 tests have passed locally.

The project also includes a separate JavaScript test file covering sample-data search, status filtering, and application counts.

**Admin logic tests:** 8 checks have passed. These test sample-data helper functions rather than the actual browser interface.

### Run Backend Tests

From the project directory:

```powershell
py -m unittest -v test_app.py
```

### Run Admin Logic Tests

```powershell
node test_admin.js
```

## Run Locally

### Requirements
- Python 3
- Git
- Node.js (for JavaScript tests)

### 1. Clone the repository

```bash
git clone https://github.com/lowski-sketch/local-business-landing-page.git
```

### 2. Enter the project directory

```bash
cd local-business-landing-page
```

### 3. Create a virtual environment

```bash
py -m venv .venv
```

### 4. Activate the environment on Windows

```powershell
.venv\Scripts\activate
```

### 5. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 6. Configure environment variables

Configure the required application settings through your local environment or hosting provider.

These include:
- `FLASK_SECRET_KEY`
- `ADMIN_PASSWORD`
- `DATABASE_URL` (optional for SQLite fallback)
- `RESEND_API_KEY` (for email delivery)
- `NOTIFICATION_EMAIL`

Never commit passwords, API keys, database credentials, or other secrets to GitHub.

### 7. Start the backend

```powershell
py app.py
```

The application uses PostgreSQL when a database URL is configured and SQLite otherwise.

## Deployment

The application uses separate hosting services:

- **Netlify:** Frontend hosting.
- **Render:** Flask backend hosting.
- **Neon:** PostgreSQL database hosting.
- **Resend:** Transactional email delivery.

Production environment variables are configured through the hosting provider rather than stored in the source repository.

## Security and Development Practices

Development practices include:
- Server-side validation of submitted information.
- Provider agreement enforcement.
- Authenticated administrator API requests.
- HTML-safe text rendering in administrator views.
- Environment-based configuration for sensitive values.
- Database separation for testing.
- Git version control.
- Automated backend tests.
- Local testing before production deployment.

The platform is an evolving application. Additional security hardening, operational monitoring, and privacy improvements remain part of the development roadmap.

## Current Development Roadmap

- Complete administrator dashboard search and filtering enhancements.
- Expand automated testing to cover actual frontend behavior.
- Develop dedicated snow-removal campaign pages and workflows.
- Improve provider lead-management functionality.
- Implement qualified-lead tracking.
- Develop provider acceptance and decline workflows.
- Improve application monitoring and operational reliability.
- Expand customer and provider onboarding.

## Skills Demonstrated

- Python application development.
- Flask backend development.
- REST API design and integration.
- PostgreSQL database integration.
- SQLite database management.
- JavaScript asynchronous programming.
- Frontend and backend integration.
- HTML and CSS responsive design.
- Email service integration.
- Authentication and input validation.
- Automated software testing.
- Git and GitHub version control.
- Cloud application deployment.
- Debugging and troubleshooting.
- Technical documentation.

## Project Direction

LocalPro is being developed as a real-world software product rather than a static portfolio demonstration.

The development process emphasizes maintainable code, practical testing, responsible deployment, and incremental improvements based on actual business requirements.