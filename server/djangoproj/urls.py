from django.contrib import admin
from django.urls import include, path

from loginuser.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("dealer_details.urls")),
    path("api/", include("reviews.urls")),
    path("api/register/", include("loginuser.urls")),
    path("api/loginuser/", LoginView.as_view(), name="loginuser"),
    path("api/logoutuser/", include("loginuser.logout_urls")),
]
