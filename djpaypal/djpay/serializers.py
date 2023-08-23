from rest_framework import serializers
from djpaypal.djpay.models import Scope, PaypalToken, PaypalInfo
from django.contrib.auth.models import User


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = "__all__"


class PaypalTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaypalToken
        fields = "__all__"


class PaypalInfoSerializer(serializers.ModelSerializer):
    scope = serializers.ListField(child=serializers.CharField(max_length=255))

    class Meta:
        model = PaypalInfo
        fields = "__all__"

    def create(self, validated_data):
        scopes_data = validated_data.pop("scope")
        user_id = validated_data.pop("user")  # Retrieve the user ID

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
