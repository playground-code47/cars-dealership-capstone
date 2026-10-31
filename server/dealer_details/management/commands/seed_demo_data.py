import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from dealer_details.models import CarMake, CarModel, Dealership
from reviews.models import Review


class Command(BaseCommand):
    help = "Add repeatable dealership demonstration data without replacing existing records."

    def handle(self, *args, **options):
        dealers = [
            ("Heartland Motors", "Wichita", "KS", "1200 E Douglas Ave", "316-555-0142", "67202", 37.6860, -97.3356),
            ("Prairie Auto Center", "Overland Park", "KS", "8400 W 135th St", "913-555-0188", "66223", 38.8814, -94.8191),
            ("Lakeside Automotive", "Chicago", "IL", "225 N Michigan Ave", "312-555-0127", "60601", 41.8864, -87.6244),
            ("Rocky Mountain Cars", "Denver", "CO", "6700 Leetsdale Dr", "303-555-0164", "80224", 39.7047, -104.9090),
            ("Desert Sky Motors", "Phoenix", "AZ", "4100 N Central Ave", "602-555-0191", "85012", 33.4484, -112.0740),
            ("Cedar Park Auto House", "Austin", "TX", "701 Congress Ave", "512-555-0140", "78701", 30.2672, -97.7431),
            ("Lone Star Motor Gallery", "Dallas", "TX", "1500 Main St", "214-555-0141", "75201", 32.7767, -96.7970),
            ("Bayou City Auto Group", "Houston", "TX", "1200 Louisiana St", "713-555-0142", "77002", 29.7604, -95.3698),
            ("Alamo City Auto Mall", "San Antonio", "TX", "300 E Commerce St", "210-555-0143", "78205", 29.4241, -98.4936),
            ("Pacific Crest Motors", "Los Angeles", "CA", "800 W Olympic Blvd", "213-555-0144", "90015", 34.0407, -118.2468),
            ("Golden Gate Auto Works", "San Diego", "CA", "100 Broadway", "619-555-0145", "92101", 32.7157, -117.1611),
            ("Silicon Valley Cars", "San Jose", "CA", "100 S Market St", "408-555-0146", "95113", 37.3382, -121.8863),
            ("Evergreen Auto Center", "Seattle", "WA", "700 5th Ave", "206-555-0147", "98104", 47.6062, -122.3321),
            ("Rose City Motors", "Portland", "OR", "100 SW Main St", "503-555-0148", "97204", 45.5152, -122.6784),
            ("Silver State Auto", "Las Vegas", "NV", "300 S 4th St", "702-555-0149", "89101", 36.1699, -115.1398),
            ("Wasatch Valley Motors", "Salt Lake City", "UT", "200 S Main St", "801-555-0150", "84101", 40.7608, -111.8910),
            ("Rio Grande Auto Plaza", "Albuquerque", "NM", "500 Tijeras Ave NW", "505-555-0151", "87102", 35.0844, -106.6504),
            ("Red Dirt Auto Exchange", "Oklahoma City", "OK", "100 W Main St", "405-555-0152", "73102", 35.4676, -97.5164),
            ("Cornhusker Motors", "Omaha", "NE", "1001 Farnam St", "402-555-0153", "68102", 41.2565, -95.9345),
            ("Hawkeye Auto Center", "Des Moines", "IA", "700 Locust St", "515-555-0154", "50309", 41.5868, -93.6250),
            ("North Star Automotive", "Minneapolis", "MN", "800 Nicollet Mall", "612-555-0155", "55402", 44.9778, -93.2650),
            ("Gateway Motor Company", "St. Louis", "MO", "100 Market St", "314-555-0156", "63101", 38.6270, -90.1994),
            ("Natural State Auto", "Little Rock", "AR", "300 President Clinton Ave", "501-555-0157", "72201", 34.7465, -92.2896),
            ("Crescent City Motors", "New Orleans", "LA", "500 Canal St", "504-555-0158", "70130", 29.9511, -90.0715),
            ("Magnolia Auto Center", "Jackson", "MS", "200 S Lamar St", "601-555-0159", "39201", 32.2988, -90.1848),
            ("Iron City Motors", "Birmingham", "AL", "200 20th St N", "205-555-0160", "35203", 33.5186, -86.8104),
            ("Peachtree Auto Gallery", "Atlanta", "GA", "200 Peachtree St NW", "404-555-0161", "30303", 33.7490, -84.3880),
            ("Biscayne Bay Motors", "Miami", "FL", "100 Biscayne Blvd", "305-555-0162", "33132", 25.7617, -80.1918),
            ("Gulf Coast Auto Works", "Tampa", "FL", "400 N Tampa St", "813-555-0163", "33602", 27.9506, -82.4572),
            ("Queen City Auto Center", "Charlotte", "NC", "200 S Tryon St", "704-555-0165", "28202", 35.2271, -80.8431),
            ("Palmetto Motor House", "Charleston", "SC", "100 Meeting St", "843-555-0166", "29401", 32.7765, -79.9311),
            ("Music City Motors", "Nashville", "TN", "200 Broadway", "615-555-0167", "37201", 36.1627, -86.7816),
            ("Bluegrass Auto Exchange", "Louisville", "KY", "100 W Main St", "502-555-0168", "40202", 38.2527, -85.7585),
            ("Queen City Automotive", "Cincinnati", "OH", "500 Vine St", "513-555-0169", "45202", 39.1031, -84.5120),
            ("Motor City Auto Group", "Detroit", "MI", "100 Renaissance Center", "313-555-0170", "48243", 42.3314, -83.0458),
            ("Crossroads Auto Gallery", "Indianapolis", "IN", "200 E Market St", "317-555-0171", "46204", 39.7684, -86.1581),
            ("Brew City Motors", "Milwaukee", "WI", "100 E Wisconsin Ave", "414-555-0172", "53202", 43.0389, -87.9065),
            ("Lake Erie Auto Center", "Cleveland", "OH", "100 Lakeside Ave E", "216-555-0173", "44114", 41.4993, -81.6944),
            ("Three Rivers Auto", "Pittsburgh", "PA", "500 Grant St", "412-555-0174", "15219", 40.4406, -79.9959),
            ("Queen City Motors", "Buffalo", "NY", "100 Delaware Ave", "716-555-0175", "14202", 42.8864, -78.8784),
            ("Empire State Auto", "New York", "NY", "100 Broadway", "212-555-0176", "10005", 40.7128, -74.0060),
            ("Harborlight Motors", "Boston", "MA", "100 Federal St", "617-555-0177", "02110", 42.3601, -71.0589),
            ("Ocean State Auto", "Providence", "RI", "100 Westminster St", "401-555-0178", "02903", 41.8240, -71.4128),
            ("Constitution Auto Center", "Hartford", "CT", "100 Pearl St", "860-555-0179", "06103", 41.7658, -72.6734),
            ("Garden State Motors", "Newark", "NJ", "100 Broad St", "973-555-0180", "07102", 40.7357, -74.1724),
            ("Liberty Bell Auto", "Philadelphia", "PA", "100 S Broad St", "215-555-0181", "19110", 39.9526, -75.1636),
            ("Chesapeake Auto Group", "Baltimore", "MD", "100 E Pratt St", "410-555-0182", "21202", 39.2904, -76.6122),
            ("Potomac Motor Company", "Arlington", "VA", "1000 Wilson Blvd", "703-555-0183", "22209", 38.8895, -77.0931),
            ("Capital City Auto House", "Washington", "DC", "1000 H St NW", "202-555-0184", "20001", 38.9072, -77.0369),
            ("Pine Tree Auto Center", "Portland", "ME", "100 Middle St", "207-555-0185", "04101", 43.6591, -70.2568),
        ]
        dealership_records = {}
        for name, city, state, address, phone, zip_code, lat, longitude in dealers:
            short_name = name
            for suffix in (
                " Motors",
                " Auto Center",
                " Automotive",
                " Auto Group",
                " Auto Gallery",
                " Auto House",
                " Auto Mall",
                " Auto Plaza",
                " Auto Works",
                " Auto Exchange",
                " Auto",
                " Cars",
            ):
                if name.endswith(suffix):
                    short_name = name[: -len(suffix)]
                    break

            defaults = {
                "city": city,
                "state": state,
                "address": address,
                "phone": phone,
                "description": f"Explore a carefully selected range of vehicles at {name}.",
                "zip": zip_code,
                "lat": lat,
                "long": longitude,
                "short_name": short_name,
                "full_name": name,
            }
            dealer, created = Dealership.objects.get_or_create(
                name=name,
                defaults=defaults,
            )
            if not created:
                missing_fields = [
                    field
                    for field in ("zip", "lat", "long", "short_name", "full_name")
                    if getattr(dealer, field) in ("", None)
                ]
                if missing_fields:
                    for field in missing_fields:
                        setattr(dealer, field, defaults[field])
                    dealer.save(update_fields=missing_fields)
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
