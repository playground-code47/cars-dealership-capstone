from django.urls import path

from .views import (
    CreateReviewView,
    analyze_review,
    analyze_review_compat,
    fetch_dealer_reviews,
    get_dealer_reviews,
)

urlpatterns = [
    path("getdealerreviews/<int:dealer_id>/", get_dealer_reviews, name="getdealerreviews"),
    path(
        "fetchReviews/dealer/<int:dealer_id>",
        fetch_dealer_reviews,
        name="fetch-reviews",
    ),
    path("fetchReviews/dealer/<int:dealer_id>/", fetch_dealer_reviews),
    path(
        "dealers/<int:dealer_id>/reviews/",
        CreateReviewView.as_view(),
        name="submit-review",
    ),
    path("analyzereview/", analyze_review, name="analyzereview"),
    path("analyze/<path:review_text>", analyze_review_compat, name="analyze-review"),
    path("analyze/<path:review_text>/", analyze_review_compat),
]
