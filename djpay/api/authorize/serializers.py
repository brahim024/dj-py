from rest_framework import serializers
from djpay.api.authorize.models import Scope, PaypalToken, PaypalInfo
from django.contrib.auth import get_user_model
import json

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
        user_id = validated_data.pop("user").id  # Retrieve the user ID
        print(user_id)
        # Get the User instance corresponding to the user ID
        user = User.objects.get(id=user_id)
        validated_data["user"] = user

        # Create the PayPalInfo instance
        paypal_info = super().create(validated_data)
        for scope_name in scopes_data:
            scope, _ = Scope.objects.get_or_create(name=scope_name)
            paypal_info.scope.add(scope)

        paypal_info.save()
        return paypal_info
