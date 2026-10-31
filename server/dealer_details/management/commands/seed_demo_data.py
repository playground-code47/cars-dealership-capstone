import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from dealer_details.models import CarMake, CarModel, Dealership
from reviews.models import Review


class Command(BaseCommand):
    help = "Create or update repeatable dealership demonstration data."

    def handle(self, *args, **options):
        dealers = [
            ("Heartland Motors", "Wichita", "KS", "1200 E Douglas Ave", "316-555-0142"),
            ("Prairie Auto Center", "Overland Park", "KS", "8400 W 135th St", "913-555-0188"),
            ("Lakeside Automotive", "Chicago", "IL", "225 N Michigan Ave", "312-555-0127"),
            ("Rocky Mountain Cars", "Denver", "CO", "6700 Leetsdale Dr", "303-555-0164"),
            ("Desert Sky Motors", "Phoenix", "AZ", "4100 N Central Ave", "602-555-0191"),
        ]
        dealership_records = {}
        for name, city, state, address, phone in dealers:
            dealer, _ = Dealership.objects.update_or_create(
                name=name,
                defaults={
                    "city": city,
                    "state": state,
                    "address": address,
                    "phone": phone,
                    "description": f"Explore a carefully selected range of vehicles at {name}.",
                },
            )
            dealership_records[name] = dealer

        makes = {
            "Toyota": ["Camry", "Corolla", "RAV4"],
            "Honda": ["Accord", "Civic", "CR-V"],
            "Ford": ["F-150", "Escape", "Mustang"],
            "Subaru": ["Outback", "Forester"],
        }
        for make_name, models in makes.items():
            make, _ = CarMake.objects.get_or_create(name=make_name)
            for model_name in models:
                CarModel.objects.get_or_create(make=make, name=model_name)

        User = get_user_model()
        reviewer, created = User.objects.get_or_create(
            username="demo_reviewer",
            defaults={"email": "reviewer@example.test"},
        )
        demo_password = os.getenv("DEMO_USER_PASSWORD")
        if created and demo_password:
            reviewer.set_password(demo_password)
            reviewer.save(update_fields=["password"])
        elif created:
            reviewer.set_unusable_password()
            reviewer.save(update_fields=["password"])

        samples = [
            ("Heartland Motors", "Friendly team and a smooth buying experience."),
            ("Prairie Auto Center", "Great selection and helpful staff."),
            ("Lakeside Automotive", "The service was excellent and straightforward."),
        ]
        for dealership_name, text in samples:
            Review.objects.get_or_create(
                dealership=dealership_records[dealership_name],
                reviewer=reviewer,
                text=text,
            )
        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
