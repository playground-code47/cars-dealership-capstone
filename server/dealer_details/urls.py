from django.urls import path

from . import views

urlpatterns = [
    path("getalldealers/", views.get_all_dealers, name="getalldealers"),
    path("getdealerbyid/<int:dealer_id>/", views.get_dealer_by_id, name="getdealerbyid"),
    path("getdealersbystate/<str:state>/", views.get_dealers_by_state, name="getdealersbyState"),
    path("getdealersbyState/<str:state>/", views.get_dealers_by_state),
    path("getallcarmakes/", views.get_all_car_makes, name="getallcarmakes"),
    path("djangoapp/get_cars", views.get_cars, name="ibm-get-cars"),
    path("djangoapp/get_cars/", views.get_cars),
    path("fetchDealers", views.get_all_dealers, name="fetch-dealers"),
    path("fetchDealers/", views.get_all_dealers),
    path("fetchDealer/<int:dealer_id>", views.get_dealer_by_id, name="fetch-dealer"),
    path("fetchDealer/<int:dealer_id>/", views.get_dealer_by_id),
    path("fetchDealers/<str:state>", views.get_dealers_by_state, name="fetch-dealers-by-state"),
    path("fetchDealers/<str:state>/", views.get_dealers_by_state),
]
