from django.urls import path, include
from .views import GenerateTokenViewSet
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"token", GenerateTokenViewSet.as_view({'post': 'create'}), basename="token")

app_name = "djpay"

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
