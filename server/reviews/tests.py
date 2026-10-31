from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from dealer_details.models import CarMake, CarModel, Dealership
from reviews.models import Review


class DealershipApiTests(TestCase):
    ibm_dealer_fields = {
        "id",
        "city",
        "state",
        "address",
        "zip",
        "lat",
        "long",
        "short_name",
        "full_name",
    }

    @classmethod
    def setUpTestData(cls):
        cls.wichita = Dealership.objects.create(
            name="Heartland Motors",
            city="Wichita",
            state="KS",
            address="1200 E Douglas Ave",
            phone="316-555-0142",
        )
        cls.denver = Dealership.objects.create(
            name="Rocky Mountain Cars",
            city="Denver",
            state="CO",
            address="6700 Leetsdale Dr",
            phone="303-555-0164",
        )
        cls.user = get_user_model().objects.create_user(
            username="reviewer", password="Str0ng-test-password!"
        )
        cls.token = Token.objects.create(user=cls.user)
        cls.review = Review.objects.create(
            dealership=cls.wichita, reviewer=cls.user, text="Fantastic service."
        )
        make = CarMake.objects.create(name="Toyota")
        CarModel.objects.create(make=make, name="Camry")

    def setUp(self):
        self.client = APIClient()

    def test_list_dealerships(self):
        response = self.client.get("/api/getalldealers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_ibm_fetch_dealers_returns_required_fields(self):
        response = self.client.get("/fetchDealers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(self.ibm_dealer_fields.issubset(response.data[0]))

    def test_ibm_fetch_dealer_returns_required_fields(self):
        response = self.client.get(f"/fetchDealer/{self.wichita.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.ibm_dealer_fields.issubset(response.data))

    def test_ibm_fetch_dealers_accepts_full_state_name(self):
        response = self.client.get("/fetchDealers/Kansas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dealer["id"] for dealer in response.data], [self.wichita.id])

    def test_ibm_fetch_dealers_accepts_state_abbreviation(self):
        response = self.client.get("/fetchDealers/KS")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dealer["id"] for dealer in response.data], [self.wichita.id])

    def test_get_dealership_by_id(self):
        response = self.client.get(f"/api/getdealerbyid/{self.wichita.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Heartland Motors")

    def test_missing_dealership_returns_404(self):
        self.assertEqual(self.client.get("/api/getdealerbyid/99999/").status_code, 404)

    def test_filter_dealerships_by_state_case_insensitive(self):
        response = self.client.get("/api/getdealersbystate/ks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dealer["state"] for dealer in response.data], ["KS"])

    def test_get_dealer_reviews_includes_reviewer(self):
        response = self.client.get(f"/api/getdealerreviews/{self.wichita.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["reviewer"], "reviewer")
        self.assertEqual(response.data[0]["text"], self.review.text)

    def test_ibm_fetch_reviews_returns_purchase_compatibility_fields(self):
        self.review.purchase = True
        self.review.purchase_date = date(2026, 10, 30)
        self.review.car_make = "Toyota"
        self.review.car_model = "Camry"
        self.review.car_year = 2024
        self.review.save()
        response = self.client.get(f"/fetchReviews/dealer/{self.wichita.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "reviewer")
        self.assertEqual(response.data[0]["dealership"], self.wichita.id)
        self.assertEqual(response.data[0]["review"], self.review.text)
        self.assertTrue(response.data[0]["purchase"])
        self.assertEqual(response.data[0]["car_make"], "Toyota")
        self.assertEqual(response.data[0]["car_model"], "Camry")
        self.assertEqual(response.data[0]["car_year"], 2024)

    def test_submit_review_requires_authentication(self):
        response = self.client.post(
            f"/api/dealers/{self.wichita.id}/reviews/", {"text": "Great visit"}
        )
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_submit_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            f"/api/dealers/{self.wichita.id}/reviews/",
            {"text": "A very helpful team"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["reviewer"], "reviewer")

    def test_authenticated_user_can_submit_purchase_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            f"/api/dealers/{self.wichita.id}/reviews/",
            {
                "text": "Great purchase.",
                "purchase": True,
                "purchase_date": "2026-10-30",
                "car_make": "Toyota",
                "car_model": "Camry",
                "car_year": 2024,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["car_make"], "Toyota")
        self.assertEqual(response.data["purchase_date"], "2026-10-30")

    def test_purchase_review_requires_purchase_details(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            f"/api/dealers/{self.wichita.id}/reviews/",
            {"text": "Great purchase.", "purchase": True},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("purchase_date", response.data)

    def test_blank_review_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            f"/api/dealers/{self.wichita.id}/reviews/", {"text": "  "}
        )
        self.assertEqual(response.status_code, 400)

    def test_list_car_makes_and_models(self):
        response = self.client.get("/api/getallcarmakes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["models"], ["Camry"])

    def test_ibm_get_cars_returns_make_model_pairs(self):
        response = self.client.get("/djangoapp/get_cars")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"CarModels": [{"CarMake": "Toyota", "CarModel": "Camry"}]},
        )

    def test_positive_review_analysis(self):
        response = self.client.post(
            "/api/analyzereview/", {"review": "Fantastic services"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["sentiment"], "positive")

    def test_ibm_get_sentiment_endpoint(self):
        response = self.client.get("/analyze/Fantastic%20services")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["sentiment"], "positive")

    def test_invalid_review_analysis_is_rejected(self):
        self.assertEqual(
            self.client.post("/api/analyzereview/", {"review": " "}).status_code,
            400,
        )

    def test_successful_login_returns_token_and_username(self):
        response = self.client.post(
            "/api/loginuser/",
            {"username": "reviewer", "password": "Str0ng-test-password!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "reviewer")
        self.assertTrue(response.data["token"])

    def test_ibm_login_uses_camel_case_credentials(self):
        response = self.client.post(
            "/djangoapp/login",
            {"userName": "reviewer", "password": "Str0ng-test-password!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"userName": "reviewer", "status": "Authenticated"})

    def test_ibm_logout_returns_empty_username(self):
        response = self.client.get("/djangoapp/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"userName": ""})

    def test_invalid_login_is_rejected(self):
        response = self.client.post(
            "/api/loginuser/", {"username": "reviewer", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_hashes_password(self):
        response = self.client.post(
            "/api/register/",
            {
                "username": "new-customer",
                "first_name": "New",
                "last_name": "Customer",
                "email": "customer@example.test",
                "password": "Long-uncommon-passphrase-938!",
            },
        )
        self.assertEqual(response.status_code, 201)
        user = get_user_model().objects.get(username="new-customer")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "Customer")
        self.assertNotEqual(user.password, "Long-uncommon-passphrase-938!")
        self.assertTrue(user.check_password("Long-uncommon-passphrase-938!"))

    def test_logout_invalidates_authentication_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post("/api/logoutuser/")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.assertEqual(
            self.client.post(
                f"/api/dealers/{self.wichita.id}/reviews/", {"text": "Again"}
            ).status_code,
            401,
        )

    def test_seed_command_is_repeatable(self):
        original_address = self.wichita.address
        original_city = self.wichita.city
        call_command("seed_demo_data")
        first_counts = (Dealership.objects.count(), Review.objects.count())
        self.assertEqual(first_counts[0], 50)
        self.assertEqual(Dealership.objects.values("name").distinct().count(), 50)
        self.assertEqual(Dealership.objects.filter(zip="").count(), 0)
        self.assertEqual(Dealership.objects.filter(lat__isnull=True).count(), 0)
        self.assertEqual(Dealership.objects.filter(long__isnull=True).count(), 0)

        self.wichita.refresh_from_db()
        self.assertEqual(self.wichita.address, original_address)
        self.assertEqual(self.wichita.city, original_city)
        self.assertEqual(self.wichita.zip, "67202")
        self.assertEqual(self.wichita.short_name, "Heartland")
        self.assertEqual(self.wichita.full_name, "Heartland Motors")

        call_command("seed_demo_data")
        self.assertEqual(
            (Dealership.objects.count(), Review.objects.count()), first_counts
        )
