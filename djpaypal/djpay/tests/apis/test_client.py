from djpaypal.djpay.client import AuthorizationAPI
from unittest.mock import patch, Mock, MagicMock
import pytest
from django.conf import settings
from djpaypal.djpay.models import PaypalToken
import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError


class TestClient:
    # test post return success when request is pass
    @patch("djpaypal.djpay.client.requests.post")
    def test_post_method(self, mock_post):
        # Create a mock response
        mock_response = Mock()
        mock_response.status_code = 200

        mock_response.json.return_value = {"key": "value"}

        # Configure the mock to return the mock response
        mock_post.return_value = mock_response

        # Create an instance of AuthorizationAPI
        api = AuthorizationAPI(api_client="client", api_secret="secret")

        # Call the post method
        response = api.post(data={}, base_url="https://example.com")

        # Assert that the mock was called with the correct arguments
        mock_post.assert_called_once_with(
            "https://example.com", {}, auth=("client", "secret"), timeout=10
        )

        # Assert that the response is as expected
        assert response.status_code == 200
        assert response.json() == {"key": "value"}

    def test_post_method_raise_without_url(self):
        # Create an instance of AuthorizationAPI
        api = AuthorizationAPI(api_client="client", api_secret="secret")
        with pytest.raises(Exception) as ex:
            api.post(data={})

        assert "Invalid URL" in str(ex.value)

    # test post raise error time out
    # @pytest.mark.django_db
    @patch("djpaypal.djpay.client.requests.post")
    def test_authorization_raise_timeout_error(self, mocker):
        mocker.exceptions = requests.exceptions
        mocker.side_effect = Timeout("Timed Out")

        auth = AuthorizationAPI("auth", "api_secret")
        result = auth.post({"grant_type", "client_credentials"}, "https://example.com")

        mocker.assert_called_once()
        # add assert called with

        assert "Timed Out" in result

    # @pytest.mark.django_db
    @patch("djpaypal.djpay.client.requests.post")
    def test_authorization_raise_connection_error(self, mocker):
        mocker.exceptions = requests.exceptions
        mocker.side_effect = ConnectionError("Connection Error")

        auth = AuthorizationAPI("auth", "api_secret")
        result = auth.post({"grant_type", "client_credentials"}, "https://example.com")

        mocker.assert_called_once()
        # add assert called with

        assert "Connection Error" in result

    # test failed status code
    @patch("djpaypal.djpay.client.requests.post")
    def test_authorization_raise_status_code_error(self, mocker):
        mocker.exceptions = requests.exceptions
        mock_response = MagicMock(status_code=403)
        mock_response.raise_for_status.side_effect = HTTPError("HttpError raised")
        mocker.return_value = mock_response

        auth = AuthorizationAPI("auth", "api_secret")
        result = auth.post({"grant_type", "client_credentials"}, "https://example.com")
        mocker.assert_called_once()
        assert "HttpError raised" in result