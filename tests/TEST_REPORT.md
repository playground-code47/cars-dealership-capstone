# Test report

Execution date: 2026-10-31 (local development environment).

## Environment

- Python 3.14.3, Django 5.2.18, Django REST Framework 3.16.1.
- Node.js and Vite 6.4.5.
- Local SQLite database with repeatable demonstration data.

## Results

| Area | Command or check | Result |
|---|---|---|
| Django | `python manage.py check` | PASS — no issues |
| Django | `python manage.py makemigrations --check --dry-run` | PASS — no changes detected |
| Database | `python manage.py migrate --check` | PASS |
| Static assets | `python manage.py collectstatic --noinput` | PASS — 163 files collected and post-processed |
| Backend | `python manage.py test` | PASS — 16 tests, 0 failures |
| Frontend | `npm test` | PASS — 5 tests across 2 files |
| Frontend | `npm run build` | PASS — Vite production build |
| Seed | `python manage.py seed_demo_data` run twice | PASS — command is repeatable |
| Static pages | `/About.html`, `/Contact.html` | PASS — HTTP 200 |
| Browser | Registration/login, dealer listing, Kansas filter, detail, review submission | PASS — live local UI flow verified |
| CORS | Request from `http://127.0.0.1:5173` to API | PASS — matching `Access-Control-Allow-Origin` |

## Live API smoke test

Nine actual response bodies are recorded in [`curl_outputs.md`](./curl_outputs.md). Registration and review creation also succeeded during the smoke test; the temporary credentials and authentication token were not recorded. Verified results:

- `loginuser`: HTTP 200.
- `logoutuser`: HTTP 200; issued token revoked.
- `getdealerreviews`, `getalldealers`, `getdealerbyid`, `getdealersbyState`, and `getallcarmakes`: HTTP 200.
- `getdealersbyState/KS/`: returned two Kansas dealerships.
- `analyzereview` for “Fantastic services”: `positive`, score `1`.
- Authenticated review submission: HTTP 201 and the new review appeared in the UI.

## Browser evidence

Eight genuine local screenshots are present in [`screenshots/`](../screenshots): both admin states, anonymous and authenticated homepages, Kansas filtering, dealer reviews, a filled review form, and the successfully added review. No deployed screenshots exist because no deployment was performed.

## Not externally verified

- GitHub Actions was authored but cannot run until the project is pushed to an authorized GitHub repository.
- Deployment is not complete; a Render account and deployment approval are required. No deployment URL is claimed.
