from django.urls import path, include
from .views import (
    GenerateTokenViewSet,
    PaypalAppTokenViewSet,
    PaypalInfoViewSet,
)
from rest_framework.routers import SimpleRouter


app_name = "authorize"


# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(
    r"generate_token", GenerateTokenViewSet, basename="generate_token"
)
router.register(
    r"token",
    PaypalAppTokenViewSet,
    basename="token",
)
router.register(r"paypal-token-info", PaypalInfoViewSet, basename="token-info")


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
