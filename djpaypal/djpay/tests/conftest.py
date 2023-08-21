import pytest

from djpaypal.djpay.models import PaypalToken
from django.conf import settings
from django.test import Client
# from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from djpaypal.djpay.views import GenerateTokenViewSet
from unittest.mock import Mock
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
def api_factory():
    return APIClient()


@pytest.fixture
def view_post():
    return GenerateTokenViewSet.as_view({'post':'create '})

@pytest.fixture
def mock_get():
    return Mock('requests.get')


@pytest.fixture
def client():
    return Client()