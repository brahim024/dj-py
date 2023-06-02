from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from .models import PaypalInfo
from .serializers import PaypalInfoSerializer


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
            return PaypalInfo.objects.filter(user=request.user)
        except PaypalInfo.DoesNotExist as e:
            return e

    def list(self, request):
        try:
            paypal_info = self.get_obj(request)
            serializer = PaypalInfoSerializer(paypal_info, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaypalInfo.DoesNotExist as e:
            return Response({"detail": e}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        obj = PaypalInfo()
        serializer = PaypalInfoSerializer(obj, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
