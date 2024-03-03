from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from djpay.api.authorize.models import PaypalInfo, PaypalToken, Scope
from .serializers import PaypalInfoSerializer
import json
from djpay.utils.client import AuthorizationAPI
from djpay.api.authorize.conf import settings as settings
from django.conf import settings as django_settings
from djpay.utils.helpers import get_paypal_token
from djpay.api.authorize.path import PayPalUrls


class PaypalAppTokenViewSet(viewsets.ViewSet):
    """
    View to display your paypal token app informations.

    * Requires basic authentication.
    * Only authenticated users are able to access this view.
    """

    

    def list(self, request):
        """
        Retrieve the access token information for the current user.
        """
        try:
            paypal_token = get_paypal_token()
            serializer = settings.SERIALIZERS.paypal_token_serializers(
                paypal_token
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except PaypalToken.DoesNotExist as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_404_NOT_FOUND
            )


class PaypalInfoViewSet(viewsets.ViewSet):
    """
    A viewset that provides access to the PayPal information of the current user.

    This viewset requires basic authentication and permission to access the user's PayPal information.
    It supports only the list action, which returns the access token and the scope of the user's PayPal account.
    """

    # Specify the authentication and permission classes
    authentication_classes = settings.AUTHENTICATION.basic_authentication
    permission_classes = settings.PERMISSIONS.is_authenticated

    def list(self, request):
        """
        * Retrieve the access token information for the current user.

        * This method tries to fetch the PaypalInfo object for the current user, which contains the access token and the scope of the user's PayPal account.
            It then serializes the object using the PaypalInfoSerializer and returns a JSON response with the serialized data and a status code of 200 (OK).
            If the PaypalInfo object does not exist for the current user, it returns a JSON response with an error message and a status code of 404 (Not Found).
        """

        try:
            # Fetch the PaypalInfo object for the current user
            obj = PaypalInfo.objects.prefetch_related("scope").all()
            # Serialize the object using the PaypalInfoSerializer
            serializer = PaypalInfoSerializer(obj, many=True)
            # Return a JSON response with the serialized data and a status code of 200 (OK)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PaypalToken.DoesNotExist as e:
            # Return a JSON response with an error message and a status code of 404 (Not Found)
            return Response(
                {"detail": str(e)}, status=status.HTTP_404_NOT_FOUND
            )


class GenerateTokenViewSet(viewsets.ViewSet):
    """
    A viewset that generates and returns a PayPal access token for the current user.

    This viewset requires basic authentication and permission to access the user's PayPal information.
    It supports only the create action, which posts a request to the PayPal API with the client credentials and the grant type.
    It then parses the response data and creates a PaypalInfo object with the access token and the scope of the user's PayPal account.
    """

    # Specify the authentication and permission classes
    authentication_classes = settings.AUTHENTICATION.basic_authentication
    permission_classes = settings.PERMISSIONS.is_authenticated

    def create(self, request, *args, **kwargs):
        """
        Generate and return a PayPal access token for the current user.

        This method tries to get the PayPal token from the settings, which contains the client ID and the client secret of the PayPal app.
        * It then constructs the URL and the extra parameters for the request to the PayPal API, using the client credentials and the grant type of "client_credentials".
        * It then creates an AuthorizationAPI object with the client ID and the client secret, and posts the request to the URL with the extra parameters and a timeout of 20 seconds.
        * If the response data is a string, it means there was an error in the request, and it returns a JSON response with the error message and a status code of 400 (Bad Request).
        * If the response data is not a string, it means the request was successful, and it loads the JSON content of the response data.
        * It then extracts the access token, the token type, the scope, the app ID, the expires in, and the nonce from the response data, and creates a dictionary with these values and the user ID.
        * It then creates a PaypalInfoSerializer object with the dictionary as the data, and validates the data.
        * If the data is valid, it saves the serializer and creates a PaypalInfo object with the access token and the scope of the user's PayPal account.
        * It then returns a JSON response with the serialized data and a status code of 201 (Created).
        * If the data is not valid, it returns a JSON response with the serializer errors and a status code of 400 (Bad Request).
        * If the PayPal token does not exist or has invalid credentials, it returns a JSON response with an error message and a status code of 404 (Not Found) or 401 (Unauthorized) respectively.
        """

        try:
            # Get the PayPal token from the settings
            get_paypal_token()
        except PaypalToken.DoesNotExist as e:
            # Return a JSON response with an error message and a status code of 404 (Not Found)
            return Response(
                {"detail": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

        # Get the base link for the PayPal API
        info = PayPalUrls.base_url()
        # Set the grant type to "client_credentials"
        grant_type = "client_credentials"
        # Construct the URL for the request
        url = info + "/v1/oauth2/token"
        # Set the extra parameters for the request
        extra = {"grant_type": grant_type}

        # Create an AuthorizationAPI object with the client ID and the client secret
        client = AuthorizationAPI(
            api_client=get_paypal_token().client_id,
            api_secret=get_paypal_token().client_secret,
        )

        # Check if the PayPal token has valid credentials
        if get_paypal_token().has_valid_token():
            # Post the request to the URL with the extra parameters and a timeout of 20 seconds
            res_data = client.post(url, extra, timeout=20)

            # Check if the response data is a string
            if isinstance(res_data, str):
                # Return a JSON response with the error message and a status code of 400 (Bad Request)
                return Response(
                    {"message": res_data}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Load the JSON content of the response data
                response_data = json.loads(res_data.content)

                # Create an empty list for the scopes
                scopes = []
                # Loop through the scope names in the response data
                for scope_name in response_data["scope"].split(" "):
                    # Append the scope name to the list
                    scopes.append(scope_name)

                # Create a dictionary with the response data and the user ID
                data = {
                    "user": request.user.id,
                    "access_token": response_data["access_token"],
                    "token_type": response_data["token_type"],
                    "scope": [{"name": s} for s in scopes],
                    "app_id": response_data["app_id"],
                    "expires_in": response_data["expires_in"],
                    "nonce": response_data["nonce"],
                }
                # Print the dictionary for debugging purposes
                print(data)

                # Create a PaypalInfoSerializer object with the data
                serializer = PaypalInfoSerializer(data=data)

                # Validate the data
                if serializer.is_valid():
                    # Save the serializer and create a PaypalInfo object
                    serializer.save()
                    # Return a JSON response with the serialized data and a status code of 201 (Created)
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                else:
                    # Return a JSON response with the serializer errors and a status code of 400 (Bad Request)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        else:
            # Return a JSON response with an error message and a status code of 401 (Unauthorized)
            return Response(
                {
                    "message": f"Your PaypalToken with name {settings.PAYPAL_TOKEN_APP_NAME} \
                        Has Not Valid credentials. \
                        Please change PAYPAL_TOKEN_APP_NAME \
                        to track another app or check current app credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


class TerminateToken(viewsets.ViewSet):
    """
    View to terminate Paypal access token.

    * Requires basic authentication.
    * Only authenticated users are able to access this view.
    """

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, reuqest):
        pass
