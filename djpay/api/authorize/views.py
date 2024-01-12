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
from django.forms.models import model_to_dict
from rest_framework.decorators import action


class PaypalAppTokenViewSet(viewsets.ViewSet):
    """
    View to display your paypal token app informations.

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
            serializer = settings.SERIALIZERS.paypal_token_serializers(
                paypal_token
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except PaypalToken.DoesNotExist as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_404_NOT_FOUND
            )


class PaypalInfoViewSet(viewsets.ViewSet):
    authentication_classes = settings.AUTHENTICATION.basic_authentication
    permission_classes = settings.PERMISSIONS.is_authenticated

    def list(self, request):
        """
        Retrieve the access token information for the current user.
        """
        try:
            obj = PaypalInfo.objects.prefetch_related("scope").all()
            serializer = PaypalInfoSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PaypalToken.DoesNotExist as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

    # def get_queryset(self):
    #     # Prefetch the related scopes for better performance
    #     return PaypalInfo.objects.prefetch_related("scope").all()


class GenerateTokenViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            get_paypal_token()
        except PaypalToken.DoesNotExist as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

        info = PaypalInfo.get_link_base()
        grant_type = "client_credentials"
        url = info + "/v1/oauth2/token"
        extra = {"grant_type": grant_type}

        client = AuthorizationAPI(
            api_client=get_paypal_token().client_id,
            api_secret=get_paypal_token().client_secret,
        )

        if get_paypal_token().has_valid_token():
            res_data = client.post(url, extra)

            if isinstance(res_data, str):
                return Response(
                    {"message": res_data}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                response_data = json.loads(res_data.content)

                # Create Scope instances
                scopes = []
                for scope_name in response_data["scope"].split(" "):
                    scopes.append(scope_name)

                data = {
                    "user": request.user.id,
                    "access_token": response_data["access_token"],
                    "token_type": response_data["token_type"],
                    "scope": [{"name": s} for s in scopes],
                    "app_id": response_data["app_id"],
                    "expires_in": response_data["expires_in"],
                    "nonce": response_data["nonce"],
                }
                print(data)

                # Create PaypalInfo instance and associate scopes
                serializer = PaypalInfoSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        else:
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
