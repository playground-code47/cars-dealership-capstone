from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CarMake, Dealership
from .serializers import CarMakeSerializer, DealershipSerializer


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
    dealers = Dealership.objects.filter(state__iexact=state.strip())
    return Response(DealershipSerializer(dealers, many=True).data)


@api_view(["GET"])
def get_all_car_makes(request):
    makes = CarMake.objects.prefetch_related("models")
    return Response(CarMakeSerializer(makes, many=True).data)
