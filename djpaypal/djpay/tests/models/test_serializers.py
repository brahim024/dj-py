from djpaypal.djpay.serializers import (
    ScopeSerializer,
    PaypalTokenSerializer,
    PaypalInfoSerializer,
)


def test_scope_serializer(db, single_scope_factory):
    scope = single_scope_factory.create()
    serializer = ScopeSerializer(scope)
    assert serializer.data["name"] == scope.name
    assert serializer.data == {"id": 1, "name": scope.name}


def test_paypal_token_serializer(db, paypal_token_factory):
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


def test_paypal_info_serializer(db, paypal_info_factory):
    info_factory = paypal_info_factory.create()
    serializer = PaypalInfoSerializer(info_factory)
    assert serializer.data["access_token"] == info_factory.access_token
