# Coursera submission checklist

Statuses reflect verified workspace facts. An unexecuted external workflow or deployment is not marked complete.

| # | Required deliverable | File location or URL | Status | Verification details |
|---:|---|---|---|---|
| 1 | README with repository/project details | [`README.md`](./README.md) | BLOCKED | README is complete locally; GitHub repository URL requires an authorized repository/push. |
| 2 | Genuine Django server output | [`django_server`](./django_server) | COMPLETE | Genuine runserver startup output captured from the running server. |
| 3 | About page GitHub URL | [`About.html`](./server/frontend/static/About.html) | BLOCKED | File is served locally (HTTP 200); GitHub URL requires repository push. |
| 4 | Contact page GitHub URL | [`Contact.html`](./server/frontend/static/Contact.html) | BLOCKED | File is served locally (HTTP 200); GitHub URL requires repository push. |
| 5 | loginuser cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual local response captured (HTTP 200); token redacted. |
| 6 | logoutuser cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual authenticated logout response captured (HTTP 200). |
| 7 | Register.jsx GitHub URL | [`Register.jsx`](./server/frontend/src/components/Register/Register.jsx) | BLOCKED | Registration file is complete and browser-tested; GitHub URL requires repository push. |
| 8 | getdealerreviews cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured (HTTP 200). |
| 9 | getalldealers cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured (HTTP 200; five seeded dealers). |
| 10 | getdealerbyid cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured (HTTP 200). |
| 11 | Kansas state-filter output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured (HTTP 200; two Kansas dealerships). |
| 12 | admin_login screenshot | [`screenshots/admin_login.png`](./screenshots/admin_login.png) | COMPLETE | Captured from the genuine Django admin login screen. |
| 13 | admin_logout screenshot | [`screenshots/admin_logout.png`](./screenshots/admin_logout.png) | COMPLETE | Captured after a real temporary admin login and logout. |
| 14 | getallcarmakes output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured with four makes and model names. |
| 15 | analyzereview output (“Fantastic services”) | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response: positive sentiment, score 1. |
| 16 | get_dealers screenshot | [`screenshots/get_dealers.png`](./screenshots/get_dealers.png) | COMPLETE | Captured from the loaded local homepage. |
| 17 | get_dealers_loggedin screenshot | [`screenshots/get_dealers_loggedin.png`](./screenshots/get_dealers_loggedin.png) | COMPLETE | Captured after successful UI registration and login. |
| 18 | dealersbystate screenshot | [`screenshots/dealersbystate.png`](./screenshots/dealersbystate.png) | COMPLETE | Live filter selected KS and showed both Kansas dealerships. |
| 19 | dealer_id_reviews screenshot | [`screenshots/dealer_id_reviews.png`](./screenshots/dealer_id_reviews.png) | COMPLETE | Captured a loaded dealer detail page with persisted reviews. |
| 20 | dealership_review_submission screenshot | [`screenshots/dealership_review_submission.png`](./screenshots/dealership_review_submission.png) | COMPLETE | Captured the actual completed review form before submission. |
| 21 | added_review screenshot | [`screenshots/added_review.png`](./screenshots/added_review.png) | COMPLETE | Captured the successful response and persisted review on the page. |
| 22 | Successful GitHub Actions result | `.github/workflows/main.yml` / GitHub Actions URL | BLOCKED | Local Git is initialized on `main`, but no remote or commit exists; an authorized GitHub destination and push are required. |
| 23 | Actual deployment URL | [`deploymentURL.txt`](./deploymentURL.txt) | BLOCKED | Requires Render account authorization and a successful deployment. |
| 24 | deployed_landingpage screenshot | [`screenshots/`](./screenshots) | BLOCKED | Requires a real deployment URL. |
| 25 | deployed_loggedin screenshot | [`screenshots/`](./screenshots) | BLOCKED | Requires a real deployment and account. |
| 26 | deployed_dealer_detail screenshot | [`screenshots/`](./screenshots) | BLOCKED | Requires a real deployment URL. |
| 27 | deployed_add_review screenshot | [`screenshots/`](./screenshots) | BLOCKED | Requires a real deployment and logged-in user. |
| 28 | End-to-end evidence bundle | [`tests/`](./tests) and [`screenshots/`](./screenshots) | COMPLETE | Local API, auth/review/browser flows, tests, outputs, and eight genuine local screenshots verified; deployed evidence is tracked separately above. |

API cURL command templates are in [`curl_commands.md`](./tests/curl_commands.md); verified test results are summarized in [`TEST_REPORT.md`](./tests/TEST_REPORT.md). No credentials, workflow results, deployment URL, or screenshot evidence are fabricated.
