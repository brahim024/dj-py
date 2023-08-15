import pytest
from djpaypal.djpay.serializers import (
    ScopeSerializer,
    PaypalTokenSerializer,
    PaypalInfoSerializer,
)


class TestSerializer:

    @pytest.mark.django_db
    def test_scope_serializer(self,single_scope_factory):
        scope = single_scope_factory.create()
        serializer = ScopeSerializer(scope)
        assert serializer.data["name"] == scope.name
        assert serializer.data == {"id": 1, "name": scope.name}

    @pytest.mark.django_db
    def test_paypal_token_serializer(self,paypal_token_factory):
        pay_token = paypal_token_factory.create()
        serializer = PaypalTokenSerializer(pay_token)
        assert serializer.data == {
            "id": pay_token.id,
            "app_name": pay_token.app_name,
            "client_id": pay_token.client_id,
            "client_secret": pay_token.client_secret,
            "user": 1,
        }
        assert serializer.data["client_id"] == pay_token.client_id

    @pytest.mark.django_db
    @pytest.mark.skip
    def test_paypal_info_serializer(self, paypal_info_factory):
        # user = user_factory.create
        info_factory = paypal_info_factory.create()
        print(info_factory.user)
        serializer = PaypalInfoSerializer(info_factory)

        assert serializer.data == {"id": info_factory.id}
        # assert serializer.data["access_token"] == info_factory.access_token
