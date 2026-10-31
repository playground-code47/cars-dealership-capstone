# Coursera submission checklist

Statuses reflect verified workspace facts. The current Phase 2+ changes are local and uncommitted; no commit, push, deployment, or new GitHub Actions run has been performed.

| # | Required deliverable | File location or URL | Status | Verification details |
|---:|---|---|---|---|
| 1 | README with repository/project details | [`README.md`](./README.md) | LOCAL UPDATE | Existing repository name remains unchanged; updated README still needs an authorized commit/push. |
| 2 | Genuine Django server output | [`django_server`](./django_server) | COMPLETE | Genuine runserver startup output captured from the running server. |
| 3 | About page GitHub URL | [`About.html`](./server/frontend/static/About.html) | LOCAL UPDATE | Three team cards and stylesheet links added; needs authorized commit/push. |
| 4 | Contact page GitHub URL | [`Contact.html`](./server/frontend/static/Contact.html) | LOCAL UPDATE | Contact details, images, active navigation, and stylesheet links added; needs authorized commit/push. |
| 5 | loginuser cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual local response captured (HTTP 200); token redacted. |
| 6 | logoutuser cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual authenticated logout response captured (HTTP 200). |
| 7 | Register.jsx GitHub URL | [`Register.jsx`](./server/frontend/src/components/Register/Register.jsx) | LOCAL UPDATE | First/last name and `Register` label are present in the workspace; not pushed. |
| 8 | getdealerreviews cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured (HTTP 200). |
| 9 | getalldealers cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | RETAKE OUTPUT | Archived output shows the prior five-dealer dataset; local database now contains 50 dealers. Capture a fresh response before submission. |
| 10 | getdealerbyid cURL output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured (HTTP 200). |
| 11 | Kansas state-filter output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured (HTTP 200; two Kansas dealerships). |
| 12 | admin_login screenshot | [`screenshots/admin_login.png`](./screenshots/admin_login.png) | COMPLETE | Captured from the genuine Django admin login screen. |
| 13 | admin_logout screenshot | [`screenshots/admin_logout.png`](./screenshots/admin_logout.png) | COMPLETE | Captured after a real temporary admin login and logout. |
| 14 | getallcarmakes output | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response captured with four makes and model names. |
| 15 | analyzereview output (“Fantastic services”) | [`curl_outputs.md`](./tests/curl_outputs.md) | COMPLETE | Actual response: positive sentiment, score 1. |
| 16 | Landing-page screenshot with URL bar | [`screenshots/get_dealers.png`](./screenshots/get_dealers.png) | RETAKE | Existing local capture has no browser URL bar; capture after deployment. |
| 17 | Logged-in dealer-list screenshot with URL bar | [`screenshots/get_dealers_loggedin.png`](./screenshots/get_dealers_loggedin.png) | RETAKE | Existing local capture has no browser URL bar; capture after deployment. |
| 18 | Kansas-filtered dealers screenshot with URL bar | [`screenshots/dealersbystate.png`](./screenshots/dealersbystate.png) | RETAKE | Existing capture has no URL bar; select Kansas in the deployed UI and recapture. |
| 19 | Dealer details and reviews screenshot with URL bar | [`screenshots/dealer_id_reviews.png`](./screenshots/dealer_id_reviews.png) | RETAKE | Existing local capture has no browser URL bar; capture the deployed dealer detail. |
| 20 | Purchase review form screenshot | [`screenshots/dealership_review_submission.png`](./screenshots/dealership_review_submission.png) | RETAKE | Existing capture predates purchase fields; show purchase selected with date, make, model, and year filled. |
| 21 | Posted review and sentiment icon screenshot | [`screenshots/added_review.png`](./screenshots/added_review.png) | RETAKE | Existing capture predates sentiment display; recapture after submitting the filled purchase review. |
| 22 | Successful GitHub Actions result for current changes | [GitHub Actions](https://github.com/playground-code47/cars-dealership-capstone/actions) | PENDING | Prior run `41214157970` succeeded for an earlier commit; these local changes have not been pushed or run in Actions. |
| 23 | Eligible IBM deployment URL | [`deploymentURL.txt`](./deploymentURL.txt) | BLOCKED | No IBM Theia/CognitiveClass workspace, IBM Cloud CLI, Code Engine credentials, or deployment project is available in this workspace. |
| 24 | Deployed landing-page screenshot | [`screenshots/`](./screenshots) | BLOCKED | Existing `ss/` capture is from Render, not an accepted IBM deployment; recapture from the actual IBM URL. |
| 25 | Deployed logged-in dealer-list screenshot | [`screenshots/`](./screenshots) | BLOCKED | Requires an actual IBM deployment and test account. |
| 26 | Deployed dealer detail screenshot | [`screenshots/`](./screenshots) | BLOCKED | Requires an actual IBM deployment. |
| 27 | Deployed purchase-review/sentiment screenshots | [`screenshots/`](./screenshots) | BLOCKED | Requires an actual IBM deployment and test account; capture the filled form and posted sentiment separately. |
| 28 | End-to-end evidence bundle | [`tests/`](./tests) and [`screenshots/`](./screenshots) | COMPLETE | Local API, auth/review/browser flows, tests, outputs, and eight genuine local screenshots verified; deployed evidence is tracked separately above. |

Retake the six screenshots in rows 16–21 with the real browser URL bar visible after deployment. Keep the form screenshot before submission and the sentiment screenshot after submission. API cURL command templates are in [`curl_commands.md`](./tests/curl_commands.md); verified test results are summarized in [`TEST_REPORT.md`](./tests/TEST_REPORT.md). No credentials, workflow results, deployment URL, or screenshot evidence are fabricated.
