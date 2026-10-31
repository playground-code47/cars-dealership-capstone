from django.urls import path

from .views import CreateReviewView, analyze_review, get_dealer_reviews

urlpatterns = [
    path("getdealerreviews/<int:dealer_id>/", get_dealer_reviews, name="getdealerreviews"),
    path(
        "dealers/<int:dealer_id>/reviews/",
        CreateReviewView.as_view(),
        name="submit-review",
    ),
    path("analyzereview/", analyze_review, name="analyzereview"),
]
