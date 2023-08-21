import pytest

from rest_framework.test import APIRequestFactory

from djpaypal.djpay.views import GenerateTokenViewSet

from pytest_factoryboy import register
from djpaypal.djpay.tests.factories import (
    ScopeFactory,
    PaypalTokenFactory,
    PaypalInfoFactory,
    SingleScopeFactory,
    UserFactory,
)

register(ScopeFactory)
register(PaypalTokenFactory)
register(PaypalInfoFactory)
register(SingleScopeFactory)
register(UserFactory)


@pytest.mark.django_db
@pytest.fixture
def paypal_token():
    return PaypalTokenFactory.create()


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def view():
    return GenerateTokenViewSet.as_view({"get": "list"})


@pytest.fixture
def view_post():
    return GenerateTokenViewSet.as_view({"post": "create"})