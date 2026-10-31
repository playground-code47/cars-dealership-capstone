# Cars Dealership Capstone

A full-stack dealership discovery and customer-review application built for the IBM Full Stack Software Developer Coursera capstone.

## Features

- Responsive React experience with dealership browsing and state filtering (including Kansas).
- Django REST API for dealerships, reviews, car makes/models, and review sentiment.
- Account registration, token login/logout, and authenticated review submission.
- Repeatable demo-data command and automated backend/frontend tests.
- GitHub Actions CI and Render deployment blueprint.

## Technology

- Python 3.12+ (verified locally with Python 3.14), Django 5.2, Django REST Framework, SQLite by default.
- React 19, React Router, Vite, and Vitest.
- Token authentication for API clients; passwords are stored using Django's password hashers.

## Run locally

Use two terminals from the project root.

### Backend

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/` and Django admin at `http://127.0.0.1:8000/admin/`.

### Frontend

```powershell
cd server\frontend
npm ci
npm run dev
```

Vite runs at `http://localhost:5173`. Copy `server/frontend/.env.example` to `server/frontend/.env` and set `VITE_API_BASE_URL` when the API is hosted elsewhere; the default is `http://127.0.0.1:8000/api`.

## Environment

Copy `.env.example` to `.env` and set a unique `SECRET_KEY` before deployment. `DEBUG` defaults to enabled for local development; set it to `False` in production. Configure `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` or `CORS_ALLOWED_ORIGIN_REGEXES`, and optionally `DATABASE_URL` for PostgreSQL. Never commit `.env` or production credentials.

The seed command creates public sample dealerships, makes, models, reviews, and an unusable-password sample reviewer. To make a login-capable seed user, set `DEMO_USER_PASSWORD` before the first seed run; the password is read only from the environment, never hard-coded.

## API

All paths below are relative to `/api/`; JSON error responses use HTTP status codes and a readable error message.

| Method | Path | Purpose |
|---|---|---|
| POST | `/register/` | Register `{ "username", "email", "password" }`; returns token and username |
| POST | `/loginuser/` | Authenticate `{ "username", "password" }`; returns token and username |
| POST | `/logoutuser/` | Revoke the current token; requires `Authorization: Token <token>` |
| GET | `/getalldealers/` | List dealerships |
| GET | `/getdealerbyid/{id}/` | Read dealership detail |
| GET | `/getdealersbystate/{state}/` | Filter by two-letter state (case-insensitive) |
| GET | `/getdealersbyState/{state}/` | Evaluation-compatible capitalization alias |
| GET | `/getdealerreviews/{id}/` | List reviews and reviewer names for a dealership |
| POST | `/dealers/{id}/reviews/` | Add `{ "text": "..." }`; requires a token |
| GET | `/getallcarmakes/` | List car makes with model names |
| POST | `/analyzereview/` | Analyze `{ "review": "Fantastic services" }` |

### cURL examples

PowerShell examples are saved in [`tests/curl_commands.md`](./tests/curl_commands.md). Actual local responses are recorded in [`tests/curl_outputs.md`](./tests/curl_outputs.md) after the backend has been started and exercised.

## Database and tests

```powershell
cd server
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo_data
python manage.py check
python manage.py test
cd frontend
npm test
npm run build
```

The backend tests use Django's isolated test database. `seed_demo_data` uses stable keys and is safe to run more than once.

## Deployment

[`render.yaml`](./render.yaml) describes a Render API service, React static site, and PostgreSQL database. Review provider pricing/availability and the generated hostnames before deploying. Deployment requires a Render account and authorization; no live URL is claimed in this workspace. After deployment, set the exact static-site origin in the API's CORS settings if the generated hostname does not match the configured origin pattern. The SQLite configuration is suitable for local development only; the blueprint uses managed PostgreSQL for persistent deployment storage.

## CI

GitHub Actions runs Django checks/tests and the frontend tests/production build for pushes and pull requests to `main` or `master`. The workflow cannot report a GitHub run until this workspace is pushed to a GitHub repository.

This workspace is initialized as a local Git repository on `main`; no remote or commit has been created. After choosing your GitHub repository and authorizing the push, connect it with:

```powershell
git remote add origin https://github.com/OWNER/REPOSITORY.git
git add .
git commit -m "Build cars dealership capstone"
git push -u origin main
```

Git may ask you to authenticate using your configured credential manager. Do not put access tokens or passwords in the repository or chat.

## Submission evidence

See [`COURsera_SUBMISSION_CHECKLIST.md`](./COURsera_SUBMISSION_CHECKLIST.md) for verified, pending, and externally blocked items and [`tests/TEST_REPORT.md`](./tests/TEST_REPORT.md) for executed validation. Screenshots are genuine local browser captures; deployed captures require a real deployment.
