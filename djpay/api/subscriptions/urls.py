from django.urls import path, include
from .views import index

# from rest_framework.routers import SimpleRouter


# Create a router and register our viewsets with it.
# router = SimpleRouter()
# router.register(r"generate-token", GenerateTokenViewSet, basename="token")

app_name = "authorize"

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("index/", index, name="index"),
]
