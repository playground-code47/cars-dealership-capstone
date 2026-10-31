from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dealer_details.models import Dealership
from .models import Review
from .serializers import ReviewSerializer

POSITIVE_WORDS = {
    "amazing", "best", "excellent", "fantastic", "friendly", "great", "helpful",
    "love", "outstanding", "positive", "recommend", "smooth", "wonderful",
}
NEGATIVE_WORDS = {
    "awful", "bad", "disappointed", "horrible", "poor", "rude", "terrible",
    "unhelpful", "worst",
}


@api_view(["GET"])
def get_dealer_reviews(request, dealer_id):
    get_object_or_404(Dealership, pk=dealer_id)
    reviews = Review.objects.filter(dealership_id=dealer_id).select_related("reviewer")
    return Response(ReviewSerializer(reviews, many=True).data)


@api_view(["GET"])
def fetch_dealer_reviews(request, dealer_id):
    get_object_or_404(Dealership, pk=dealer_id)
    reviews = Review.objects.filter(dealership_id=dealer_id).select_related("reviewer")
    return Response(
        [
            {
                "name": review.reviewer.username,
                "dealership": review.dealership_id,
                "review": review.text,
                "purchase": review.purchase,
                "purchase_date": review.purchase_date,
                "car_make": review.car_make,
                "car_model": review.car_model,
                "car_year": review.car_year,
            }
            for review in reviews
        ]
    )


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        dealership = get_object_or_404(Dealership, pk=self.kwargs["dealer_id"])
        serializer.save(dealership=dealership, reviewer=self.request.user)


@api_view(["POST"])
def analyze_review(request):
    text = request.data.get("review", request.data.get("text", ""))
    if not isinstance(text, str) or not text.strip():
        return Response(
            {"error": "Provide non-empty review text."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    words = {word.strip(".,!?;:()[]{}\"'").lower() for word in text.split()}
    score = len(words & POSITIVE_WORDS) - len(words & NEGATIVE_WORDS)
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return Response({"sentiment": sentiment, "score": score})


@api_view(["GET"])
def analyze_review_compat(request, review_text):
    words = {word.strip(".,!?;:()[]{}\"'").lower() for word in review_text.split()}
    score = len(words & POSITIVE_WORDS) - len(words & NEGATIVE_WORDS)
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return Response({"sentiment": sentiment})
