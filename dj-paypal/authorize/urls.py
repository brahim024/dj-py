from django.urls import path
from .views import ListUsers

app_name='authorize'

urlpatterns = [
    path('', ListUsers.as_view(), name='list-users')
]
