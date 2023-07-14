from djpaypal.djpay.client import AuthorizationAPI
from unittest.mock import patch, Mock


@patch("requests.post")
def test_post_method(mock_post):
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
