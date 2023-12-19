from django.urls import path, include
from .views import GenerateTokenViewSet
from rest_framework.routers import SimpleRouter


# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(r"generate-token", GenerateTokenViewSet, basename="token")

app_name = "djpay"

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
