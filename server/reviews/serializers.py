from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.CharField(source="reviewer.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "dealership", "reviewer", "text", "created_at"]
        read_only_fields = ["id", "dealership", "reviewer", "created_at"]

    def validate_text(self, value):
        text = value.strip()
        if not text:
            raise serializers.ValidationError("Review text cannot be blank.")
        return text
