from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from djpaypal.djpay.models import PaypalInfo, PaypalToken
from .serializers import PaypalInfoSerializer, PaypalTokenSerializer
import requests
import json
from djpaypal.djpay.client import AuthorizationAPI
from djpaypal.djpay.conf import settings
from djpaypal.djpay.helpers import get_paypal_token


class GenerateTokenViewSet(viewsets.ViewSet):
    """
    View to generate Paypal access token.

    * Requires basic authentication.
    * Only authenticated users are able to access this view.
    """

    authentication_classes = settings.AUTHENTICATION.basic_authentication
    permission_classes = settings.PERMISSIONS.is_authenticated

    def list(self, request):
        """
        Retrieve the access token information for the current user.
        """
        try:
            paypal_token = get_paypal_token()
            serializer = settings.SERIALIZERS.paypal_token_serializers(paypal_token)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except PaypalToken.DoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Create a new access token using the provided client credentials.
        """

        try:
            get_paypal_token()
        except PaypalToken.DoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        info = PaypalInfo.get_link_base()
        grant_type = "client_credentials"
        url = info + "/v1/oauth2/token"
        body_params = {"grant_type": grant_type}

        client = AuthorizationAPI(
            api_client=get_paypal_token().client_id,
            api_secret=get_paypal_token().client_secret,
        )

        if get_paypal_token().has_valid_token():
            res_data = client.post(body_params, url, timeout=20)
            print("res_data: ", res_data)

            if isinstance(res_data, str):
                return Response(
                    {"message": res_data}, status=status.HTTP_400_BAD_REQUEST
                )
            else:

                response_data = json.loads(res_data.content)
                scopes = [s for s in response_data["scope"].split(" ")]

                data = {
                    "user": request.user.id,
                    "scope": scopes,
                    "access_token": response_data["access_token"],
                    "token_type": response_data["token_type"],
                    "app_id": response_data["app_id"],
                    "expires_in": response_data["expires_in"],
                    "nonce": response_data["nonce"],
                }

                serializer = PaypalInfoSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.create(validated_data=data)
                    try:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response(
                            serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                return Response(
                    serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    "message": f"Your PaypalToken with name {settings.PAYPAL_TOKEN_APP_NAME}\
                     Has Not Valid credentials.\
                    Please change PAYPAL_TOKEN_APP_NAME\
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
