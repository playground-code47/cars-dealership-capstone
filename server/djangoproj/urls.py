from django.contrib import admin
from django.urls import include, path

from dealer_details import views as dealer_views
from loginuser.views import LoginView, ibm_login, ibm_logout
from reviews.views import analyze_review_compat, fetch_dealer_reviews

urlpatterns = [
    path("admin/", admin.site.urls),
    path("fetchDealers", dealer_views.get_all_dealers, name="ibm-fetch-dealers"),
    path("fetchDealers/", dealer_views.get_all_dealers),
    path("fetchDealer/<int:dealer_id>", dealer_views.get_dealer_by_id, name="ibm-fetch-dealer"),
    path("fetchDealer/<int:dealer_id>/", dealer_views.get_dealer_by_id),
    path("fetchDealers/<str:state>", dealer_views.get_dealers_by_state, name="ibm-fetch-dealers-by-state"),
    path("fetchDealers/<str:state>/", dealer_views.get_dealers_by_state),
    path("djangoapp/login", ibm_login, name="ibm-login"),
    path("djangoapp/login/", ibm_login),
    path("djangoapp/logout", ibm_logout, name="ibm-logout"),
    path("djangoapp/logout/", ibm_logout),
    path("djangoapp/get_cars", dealer_views.get_cars, name="ibm-get-cars-root"),
    path("djangoapp/get_cars/", dealer_views.get_cars),
    path(
        "fetchReviews/dealer/<int:dealer_id>",
        fetch_dealer_reviews,
        name="ibm-fetch-reviews",
    ),
    path("fetchReviews/dealer/<int:dealer_id>/", fetch_dealer_reviews),
    path("analyze/<path:review_text>", analyze_review_compat, name="ibm-analyze"),
    path("analyze/<path:review_text>/", analyze_review_compat),
    path("api/", include("dealer_details.urls")),
    path("api/", include("reviews.urls")),
    path("api/register/", include("loginuser.urls")),
    path("api/loginuser/", LoginView.as_view(), name="loginuser"),
    path("api/logoutuser/", include("loginuser.logout_urls")),
]
