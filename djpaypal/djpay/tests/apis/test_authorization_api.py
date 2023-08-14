import unittest
from unittest.mock import MagicMock
import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from djpaypal.djpay.views import GenerateTokenViewSet
from djpaypal.djpay.models import PaypalInfo
from rest_framework.test import APIRequestFactory




class TestAPiClient:
        
    def test_list_access_api_without_authentication(self,db):
        client = Client()
        client_url = reverse("djpay:token-list")
        response = client.get(path=client_url)
        assert response.status_code == 401



    def test_generate_access_token_list(self,db,view,user_factory,factory,paypal_token):
        print("User Factory: ",user_factory)
        request = factory.get(reverse("djpay:token-list"))
        force_authenticate(request, user=user_factory.create())

        response = view(request)
        response.status_code == 200
        response.data["client_id"] == paypal_token.client_id



    @pytest.mark.skip
    def test_generate_access_token_post_with_unvalid_credentials(
        self,db,user_factory, factory, view_post, paypal_token
        ):
        assert PaypalInfo.objects.all().count() == 0
        request = factory.post(reverse("djpay:token-post"))
        force_authenticate(request, user=user_factory.create())
        response = view_post(request)
        assert PaypalInfo.objects.all().count() == 0