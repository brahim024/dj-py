import pytest
from django.urls import reverse
from django.test import Client
from rest_framework.test import force_authenticate
from djpaypal.djpay.models import PaypalInfo
import requests
from unittest.mock import patch
from requests.exceptions import ConnectionError


class TestAPiClient:
    def test_list_access_api_without_authentication(self):
        client = Client()
        client_url = reverse("djpay:token-list")
        response = client.get(path=client_url)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_generate_access_token_list(
        self, user_factory, view, factory, paypal_token
    ):
        request = factory.get(reverse("djpay:token-list"))
        force_authenticate(request, user=user_factory.create())

        response = view(request)
        response.status_code == 200

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_generate_access_token_post_with_unvalid_credentials(
        self, user_factory, factory, view_post, paypal_token
    ):
        assert PaypalInfo.objects.all().count() == 0
        request = factory.post(reverse("djpay:token-create"))
        force_authenticate(request, user=user_factory.create())
        view_post(request)
        assert PaypalInfo.objects.all().count() == 0

    @pytest.mark.django_db
    @patch("djpaypal.djpay.models.requests.post")
    def test_has_valid_token_raise_connection_error(self, mocker, paypal_token_factory):
        mocker.exceptions = requests.exceptions
        mocker.side_effect = ConnectionError("Connection Error")

        token = paypal_token_factory.create()

        # add assert called with
        assert "Connection Error" in token.has_valid_token()