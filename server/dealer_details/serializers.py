from rest_framework import serializers

from .models import CarMake, Dealership


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = ["id", "name", "city", "state", "address", "phone", "description"]


class CarMakeSerializer(serializers.ModelSerializer):
    models = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = CarMake
        fields = ["id", "name", "models"]
