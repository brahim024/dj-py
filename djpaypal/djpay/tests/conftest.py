from pytest_factoryboy import register
from djpaypal.djpay.tests.factories import (
    ScopeFactory,
    PaypalTokenFactory,
    PaypalInfoFactory,
    SingleScopeFactory,
)

register(ScopeFactory)
register(PaypalTokenFactory)
register(PaypalInfoFactory)
register(SingleScopeFactory)
