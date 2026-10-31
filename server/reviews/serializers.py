from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CharField(source="reviewer.username", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "dealership",
            "reviewer",
            "text",
            "purchase",
            "purchase_date",
            "car_make",
            "car_model",
            "car_year",
            "created_at",
        ]
        read_only_fields = ["id", "dealership", "reviewer", "created_at"]

    def validate_text(self, value):
        text = value.strip()
        if not text:
            raise serializers.ValidationError("Review text cannot be blank.")
        return text

    def validate(self, attrs):
        if attrs.get("purchase", False):
            required_fields = ("purchase_date", "car_make", "car_model", "car_year")
            missing_fields = [
                field for field in required_fields if not attrs.get(field)
            ]
            if missing_fields:
                raise serializers.ValidationError(
                    {
                        field: "This field is required for a purchase review."
                        for field in missing_fields
                    }
                )
        return attrs
