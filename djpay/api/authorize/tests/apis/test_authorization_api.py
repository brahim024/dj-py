import pytest
from django.urls import reverse
from django.test import Client
from djpay.api.authorize.models import PaypalInfo
import requests
from djpay.api.authorize.views import PaypalAppTokenViewSet

from unittest.mock import patch
from requests.exceptions import ConnectionError


class TestTokenApp:
    
    @pytest.mark.django_db
    def test_list_access_api_without_asuthetication(self,api_client):
        
        response = api_client.get(path="http://127.0.0.1:8000/djpay/token/")
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_list_access_api_without_token_app(self,api_client,user_factory):
        user = user_factory.create()
        api_client.force_authenticate(user=user)
        response = api_client.get(path="http://127.0.0.1:8000/djpay/token/")
        # response = views(request.data)
        assert response.data['detail'] == 'PaypalToken matching query does not exist.'
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_list_access_api_with_token_app(self,api_client,paypal_token_factory,user_factory):
        user = user_factory.create()
        token_app = paypal_token_factory.create(user=user)
        api_client.force_authenticate(user=user)
        response = api_client.get(path="http://127.0.0.1:8000/djpay/token/")
        
        # response = views(request.data)
        assert response.status_code == 200

    

class TestPaypalInfo:
    """
    in this case I'll mock the request that is comming from paypal then make a test 
    """
    @pytest.mark.django_db
    def test_generate_access_token_post_with_unvalid_credentials(
        self, user_factory, api_client, paypal_token,paypal_info_factory
    ):
        assert PaypalInfo.objects.all().count() == 0
        user = user_factory.create()
        api_client.force_authenticate(user=user)
        
        request = api_client.post(path="http://127.0.0.1:8000/djpay/generate_token/")
        print("Response: ",request)


    @pytest.mark.skip
    @pytest.mark.django_db
    @patch("djpay.api.authorize.models.requests.post")
    def test_has_valid_token_raise_connection_error(
        self, mocker, paypal_token_factory
    ):
        mocker.exceptions = requests.exceptions
        mocker.side_effect = ConnectionError("Connection Error")

        token = paypal_token_factory.create()

        # add assert called with
        assert "Connection Error" in token.has_valid_token()
