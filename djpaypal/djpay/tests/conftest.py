from pytest_factoryboy import register
from djpaypal.djpay.tests.factories import (
    ScopeFactory,
    PaypalTokenFactory,
    PaypalInfoFactory,
    SingleScopeFactory,
    UserFactory
)

register(ScopeFactory)
register(PaypalTokenFactory)
register(PaypalInfoFactory)
register(SingleScopeFactory)
register(UserFactory)