from django.urls import path, include
from .views import (
    GenerateTokenViewSet,
    PaypalAppTokenViewSet,
    PaypalInfoViewSet,
)
from rest_framework.routers import SimpleRouter


# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(
    r"generate-token", GenerateTokenViewSet, basename="generate-token"
)
router.register(
    r"paypal-app-token",
    PaypalAppTokenViewSet,
    basename="display-app-token",
)
router.register(r"paypal-token-info", PaypalInfoViewSet, basename="token-info")
app_name = "authorize"

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
