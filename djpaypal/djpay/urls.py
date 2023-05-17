from django.urls import path
from . import views

app_name = "djpy"

urlpatterns = [path("", views.index, name="index")]
