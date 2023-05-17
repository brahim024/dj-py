import pytest
from pytest_factoryboy import register
from djpaypal.djpay.tests.factories import ScopeFactory, PaypalTokenFactory

register(ScopeFactory)
register(PaypalTokenFactory)
