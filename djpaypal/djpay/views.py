from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from .models import PaypalInfo, PaypalToken, Scope
from .serializers import PaypalInfoSerializer, PaypalTokenSerializer
import requests
import json
from .client import AuthorizationlAPI

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
            return PaypalToken.objects.get(user=request.user)
        except PaypalInfo.DoesNotExist as e:
            return e

    def list(self, request):
        try:
            paypal_token = self.get_obj(request)
            serializer = PaypalTokenSerializer(paypal_token, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaypalToken.DoesNotExist as e:
            return Response({"detail": e}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        token_obj = self.get_obj(request)
        info = PaypalInfo.get_link_base()
        grant_type = "client_credentials"
        url = info + "/v1/oauth2/token"
        body_params = {"grant_type": grant_type}

        client = AuthorizationlAPI(
            api_client=token_obj.client_id, api_secret=token_obj.client_secret
        )
        try:
            res_data = client.post(body_params, url, timeout=20)
        except Exception as e:
            return Response({"message": str(e)})
        # response = requests.post(url, data=body_params, auth=(token_obj.client_id, token_obj.client_secret))
        # res_data = json.loads(response.text)
        # create scopes
        scopes = [s for s in res_data["scope"].split(" ")]
        data = {
            "user": request.user.id,
            "scope": scopes,
            "access_token": res_data["access_token"],
            "token_type": res_data["token_type"],
            "app_id": res_data["app_id"],
            "expires_in": res_data["expires_in"],
            "nonce": res_data["nonce"],
        }

        serializer = PaypalInfoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(validated_data=data)
            try:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(
                    serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
