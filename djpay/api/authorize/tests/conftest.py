import pytest

from rest_framework.test import APIRequestFactory

from djpay.api.authorize.views import GenerateTokenViewSet

from rest_framework.test import APIClient  

from pytest_factoryboy import register
from djpay.api.authorize.tests.factories import (
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


  
@pytest.fixture(scope="function")  
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    :return: APIClient  
    """  
    return APIClient()


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def view():
    return GenerateTokenViewSet.as_view({"get": "list"})


@pytest.fixture
def view_post():
    return GenerateTokenViewSet.as_view({"post": "create"})
