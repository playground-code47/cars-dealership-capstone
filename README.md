# Cars Dealership Capstone

A full-stack dealership discovery and customer-review application built for the IBM Full Stack Software Developer Coursera capstone.

**GitHub repository:** [playground-code47/cars-dealership-capstone](https://github.com/playground-code47/cars-dealership-capstone)

## Features

- Responsive React experience with dealership browsing and state filtering (including Kansas).
- Django REST API with the existing `/api/` endpoints and IBM-compatible routes for dealerships, reviews, cars, authentication, and sentiment.
- Account registration, token login/logout, and authenticated reviews with optional purchase date and vehicle details.
- Repeatable seed command for 50 dealerships and automated backend/frontend tests.
- Independent Python and JavaScript lint jobs, plus the existing CI workflow and Render blueprint.

## Technology

- Python 3.12+ (verified locally with Python 3.14), Django 5.2, Django REST Framework, SQLite by default.
- React 19, React Router, Vite, Vitest, and ESLint.
- Token authentication for API clients; passwords are stored using Django's password hashers.

## Architecture

- `server/djangoproj/` configures Django, middleware, database settings, and root URL routes.
- `server/dealer_details/` contains dealership/car models, APIs, migrations, and the repeatable seed command.
- `server/reviews/` contains review models, serializers, sentiment APIs, and backend tests.
- `server/loginuser/` contains account registration, token authentication, and IBM-compatible login/logout routes.
- `server/frontend/` contains the React/Vite application, static About/Contact pages, frontend tests, and lint configuration.

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

The seed command creates 50 public sample dealerships, makes, models, reviews, and an unusable-password sample reviewer. It adds missing dealership records without deleting existing rows and fills only missing dealer metadata. To make a login-capable seed user, set `DEMO_USER_PASSWORD` before the first seed run; the password is read only from the environment, never hard-coded.

## API

All paths in the first table are relative to `/api/`; JSON error responses use HTTP status codes and a readable error message.

| Method | Path | Purpose |
|---|---|---|
| POST | `/register/` | Register `{ "username", "first_name", "last_name", "email", "password" }`; returns token and username |
| POST | `/loginuser/` | Authenticate `{ "username", "password" }`; returns token and username |
| POST | `/logoutuser/` | Revoke the current token; requires `Authorization: Token <token>` |
| GET | `/getalldealers/` | List dealerships |
| GET | `/getdealerbyid/{id}/` | Read dealership detail |
| GET | `/getdealersbystate/{state}/` | Filter by state abbreviation or full name (case-insensitive) |
| GET | `/getdealersbyState/{state}/` | Evaluation-compatible capitalization alias |
| GET | `/getdealerreviews/{id}/` | List reviews and reviewer names for a dealership |
| POST | `/dealers/{id}/reviews/` | Add a review with optional purchase metadata; requires a token |
| GET | `/getallcarmakes/` | List car makes with model names |
| POST | `/analyzereview/` | Analyze `{ "review": "Fantastic services" }` |

IBM-compatible routes are registered at the application root (not under `/api/`):

| Method | Path | Purpose |
|---|---|---|
| GET | `/fetchDealers` | List dealers with `id`, `city`, `state`, `address`, `zip`, `lat`, `long`, `short_name`, and `full_name` |
| GET | `/fetchDealer/{id}` | Return one dealer in the same response shape |
| GET | `/fetchDealers/{state}` | Filter by state abbreviation or full state name, e.g. `Kansas` |
| GET | `/fetchReviews/dealer/{id}` | List IBM-compatible reviews, including purchase and vehicle fields |
| POST | `/djangoapp/login` | Accept `{ "userName", "password" }`; returns `{ "userName", "status": "Authenticated" }` on success |
| GET | `/djangoapp/logout` | Return `{ "userName": "" }` |
| GET | `/djangoapp/get_cars` | Return a `CarModels` array of `CarMake`/`CarModel` pairs |
| GET | `/analyze/{review_text}` | Analyze URL-encoded review text, e.g. `/analyze/Fantastic%20services` |

For purchase reviews, include `purchase: true`, `purchase_date`, `car_make`, `car_model`, and `car_year`. Existing review POSTs can omit these fields or send `purchase: false`.

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
npm run lint
```

The backend tests use Django's isolated test database. `seed_demo_data` uses stable keys and is safe to run more than once.

## Deployment

[`render.yaml`](./render.yaml) describes a Render API service, React static site, and PostgreSQL database. To deploy it manually:

1. Sign in to Render and connect the GitHub account that can access this repository.
2. Choose **New → Blueprint**, select `playground-code47/cars-dealership-capstone`, and use the `main` branch.
3. Review the services and current pricing before applying the blueprint. The database and web service may incur charges.
4. Apply the blueprint and wait for both API and frontend builds to finish.
5. Confirm the API responds at `https://<api-service-host>/api/getalldealers/`. Open the frontend URL and register a real user to test login and review submission.
6. If the generated frontend hostname does not match `CORS_ALLOWED_ORIGIN_REGEXES`, set `CORS_ALLOWED_ORIGINS` on the API service to the exact frontend origin (for example `https://<static-site-host>`), then redeploy the API.
7. Record the real frontend deployment URL in [`deploymentURL.txt`](./deploymentURL.txt) and capture deployed screenshots only after verifying the live pages.

The blueprint sets `DEBUG=False`, creates a secret key, configures the API host, and uses managed PostgreSQL for persistent data. Review/adjust the generated hostnames and environment settings before launch. SQLite is for local development only. No account credentials, payment approval, deployment, or live URL are assumed.

### IBM deployment and screenshots

No IBM Theia/CognitiveClass workspace, IBM Cloud CLI, Code Engine credentials, or eligible deployment project is configured in this repository workspace. Do not treat the Render URL as an IBM deployment. To complete an IBM-hosted submission, sign in to the IBM Theia/CognitiveClass environment supplied by the course, or obtain an IBM Cloud account and Code Engine access; deploy the app there, configure a persistent PostgreSQL `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`, allowed hosts, and frontend CORS, then record only the URL that actually loads.

After a real deployment, retake genuine browser screenshots with the browser's URL bar visible:

1. Landing page.
2. Logged-in dealer list.
3. Dealer list filtered to Kansas.
4. Dealer detail with existing reviews.
5. Review form with purchase selected and date, make, model, and year filled.
6. Newly posted review showing the sentiment icon.

Use the real deployed URL and a test account you control. Keep the form screenshot before submission and the posted-review screenshot after submission. Do not reuse the older screenshots as proof of the updated purchase/sentiment workflow.

## CI

GitHub Actions runs Django checks/tests and the frontend tests/production build for pushes and pull requests to `main` or `master`. [View workflow runs](https://github.com/playground-code47/cars-dealership-capstone/actions).

This workspace is connected to the `main` branch of the repository above. To publish later changes:

```powershell
git add .
git commit -m "Describe your changes"
git push -u origin main
```

Git may ask you to authenticate using your configured credential manager. Do not put access tokens or passwords in the repository or chat.

## Submission evidence

See [`COURsera_SUBMISSION_CHECKLIST.md`](./COURsera_SUBMISSION_CHECKLIST.md) for verified, pending, and externally blocked items and [`tests/TEST_REPORT.md`](./tests/TEST_REPORT.md) for executed validation. Screenshots are genuine local browser captures; deployed captures require a real deployment.
