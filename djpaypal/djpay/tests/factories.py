import factory
from djpaypal.djpay.models import Scope, PaypalToken
from faker import Faker

faker = Faker()


class ScopeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Scope

    name = faker.uri()


class PaypalTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaypalToken

    app_name = faker.domain_name()
    client_id = faker.nic_handle()
    client_secret = faker.pystr()
