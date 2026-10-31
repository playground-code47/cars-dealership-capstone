# Test report

Execution date: 2026-10-31 (local development environment).

## Current validation

| Area | Command or check | Result |
|---|---|---|
| Django | `python manage.py check` | PASS — no issues |
| Migrations | `python manage.py makemigrations --check --dry-run` | PASS — no pending model changes |
| Migrations | `python manage.py migrate` | PASS — additive dealer and review migrations applied |
| Backend | `python manage.py test` | PASS — 27 tests, 0 failures |
| Frontend | `npm test` | PASS — 5 tests across 2 files |
| Python lint | `python -m ruff check --select E4,E7,E9,F server` | PASS |
| JavaScript lint | `npm run lint` | PASS — ESLint |
| Frontend build | `npm run build` | PASS — Vite production build |
| Seed | `python manage.py seed_demo_data` | PASS — 50 distinct dealers, 8 reviews, 4 makes, and 11 models; no missing dealer ZIPs or coordinates |
| Lint workflow | YAML parse and job inspection | PASS — two independent jobs; both include a `Run Linter` step |

The backend tests cover the existing `/api/` endpoints, IBM-compatible dealer/review/auth/cars/sentiment endpoints, purchase-review persistence/validation, and repeatable seeding. The frontend test exercises registration names and the purchase-review workflow through sentiment display.

## Database preservation

The migrations add nullable/defaulted fields and preserve existing dealership and review rows. The seed command uses stable dealer names and `get_or_create`; it does not delete records. The local database contains 50 unique dealerships and 8 reviews after the run. The existing database backup was not modified.

## Archived cURL output

[`curl_outputs.md`](./curl_outputs.md) contains genuine local responses captured before the dataset was expanded from five dealerships to 50. It remains an archive, not a current 50-dealer response transcript. Use the updated commands in [`curl_commands.md`](./curl_commands.md) to capture current output.

## Screenshots and deployment

Existing screenshots are retained, but the page screenshots do not show browser URL bars and the review screenshots predate purchase metadata and sentiment display. Retake the landing page, logged-in dealer list, Kansas filter, dealer detail, filled purchase-review form, and posted-review/sentiment captures after an eligible deployment; keep the actual URL bar visible.

No IBM Theia/CognitiveClass workspace or IBM Code Engine credentials/project are available in this local environment. The previous GitHub Actions run succeeded for an earlier commit, but current changes have not been pushed and have no corresponding Actions run. No deployment URL or deployed screenshot is claimed.
