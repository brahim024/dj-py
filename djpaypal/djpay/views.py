from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from .models import PaypalInfo, PaypalToken
from .serializers import PaypalInfoSerializer, PaypalTokenSerializer
import requests
import json
from .client import AuthorizationAPI
from django.conf import settings


# Create your views here.
# def index(request):
#     return HttpResponse("Hello")


class GenerateTokenViewSet(viewsets.ViewSet):
    """
    View to generate Paypal access token.

    * Requires basic authentication.
    * Only authenticated users are able to access this view.
    """

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_obj(self, request):
        try:
            return PaypalToken.objects.get(pk=settings.PAYPAL_TOKEN_ID)
        except PaypalInfo.DoesNotExist as e:
            return e

    def list(self, request):
        try:
            paypal_token = self.get_obj(request)
            serializer = PaypalTokenSerializer(paypal_token, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaypalToken.DoesNotExist as e:
            return Response({"detail": e}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            token_obj = self.get_obj(request)
        except PaypalToken.DoesNotExist as e:
             return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        info = PaypalInfo.get_link_base()
        grant_type = "client_credentials"
        url = info + "/v1/oauth2/token"
        body_params = {"grant_type": grant_type}

        client = AuthorizationAPI(
            api_client=token_obj.client_id, api_secret=token_obj.client_secret
        )
        try:
            res_data = client.post(body_params, url, timeout=20)
        except requests.exceptions.RequestException as e:
            return Response({"message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        response_data = json.loads(res_data.text)
        # create scopes
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
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(
                    serializer.error_messages,
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)
