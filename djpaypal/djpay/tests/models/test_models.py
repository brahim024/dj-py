import pytest
from djpaypal.djpay.models import Scope, PaypalToken


def test_scope_factory_create(db, scope_factory):
    scope_factory.create()
    assert Scope.objects.all().count() == 1


def test_scope_representation(db):
    scope = Scope.objects.create(name="test")
    assert str(scope) == "test"


def test_paypal_token_create(db, paypal_token_factory):
    assert PaypalToken.objects.all().count() == 0
    paypal_token_factory.create()
    assert PaypalToken.objects.all().count() == 1
