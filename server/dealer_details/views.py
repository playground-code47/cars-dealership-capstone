from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CarMake, Dealership
from .serializers import CarMakeSerializer, DealershipSerializer


STATE_ABBREVIATIONS = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "district of columbia": "DC",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
}


@api_view(["GET"])
def get_all_dealers(request):
    dealers = Dealership.objects.all()
    return Response(DealershipSerializer(dealers, many=True).data)


@api_view(["GET"])
def get_dealer_by_id(request, dealer_id):
    dealer = get_object_or_404(Dealership, pk=dealer_id)
    return Response(DealershipSerializer(dealer).data)


@api_view(["GET"])
def get_dealers_by_state(request, state):
    normalized_state = state.strip()
    state_abbreviation = STATE_ABBREVIATIONS.get(
        normalized_state.casefold(), normalized_state.upper()
    )
    dealers = Dealership.objects.filter(state__iexact=state_abbreviation)
    return Response(DealershipSerializer(dealers, many=True).data)


@api_view(["GET"])
def get_all_car_makes(request):
    makes = CarMake.objects.prefetch_related("models")
    return Response(CarMakeSerializer(makes, many=True).data)


@api_view(["GET"])
def get_cars(request):
    car_models = [
        {"CarMake": make.name, "CarModel": model.name}
        for make in CarMake.objects.prefetch_related("models")
        for model in make.models.all()
    ]
    return Response({"CarModels": car_models})
