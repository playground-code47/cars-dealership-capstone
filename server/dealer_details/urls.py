from django.urls import path

from . import views

urlpatterns = [
    path("getalldealers/", views.get_all_dealers, name="getalldealers"),
    path("getdealerbyid/<int:dealer_id>/", views.get_dealer_by_id, name="getdealerbyid"),
    path("getdealersbystate/<str:state>/", views.get_dealers_by_state, name="getdealersbyState"),
    path("getdealersbyState/<str:state>/", views.get_dealers_by_state),
    path("getallcarmakes/", views.get_all_car_makes, name="getallcarmakes"),
]
