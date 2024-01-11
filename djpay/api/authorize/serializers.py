from rest_framework import serializers
from djpay.api.authorize.models import Scope, PaypalToken, PaypalInfo
from django.contrib.auth import get_user_model

User = get_user_model()


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ["name"]


class PaypalTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalToken
        fields = "__all__"


class PaypalInfoSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    scope = ScopeSerializer(many=True)

    class Meta:
        model = PaypalInfo
        fields = "__all__"

    def create(self, validated_data):
        scopes_data = validated_data.pop("scope")
        paypal_info = PaypalInfo.objects.create(**validated_data)
        for scope_data in scopes_data:
            scope, _ = Scope.objects.get_or_create(**scope_data)
            paypal_info.scope.add(scope)
        return paypal_info

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["scope"] = [s.name for s in instance.scope.all()]
        return data
