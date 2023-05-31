from rest_framework import serializers
from .models import Scope, PaypalToken, PaypalInfo


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = "__all__"


class PaypalTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalToken
        fields = "__all__"


class PaypalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalInfo
        fields = "__all__"
