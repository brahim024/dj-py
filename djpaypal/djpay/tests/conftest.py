import pytest
from pytest_factoryboy import register
from djpaypal.djpay.tests.factories import (
    ScopeFactory,
    PaypalTokenFactory,
    PaypalInfoFactory,
)

register(ScopeFactory)
register(PaypalTokenFactory)
register(PaypalInfoFactory)
