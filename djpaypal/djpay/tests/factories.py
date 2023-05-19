import factory
from djpaypal.djpay.models import Scope, PaypalToken, PaypalInfo
from faker import Faker

fake = Faker()


class ScopeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Scope

    name = factory.Sequence(lambda n: f"Scope {n}")


class PaypalTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaypalToken

    app_name = fake.domain_name()
    client_id = fake.nic_handle()
    client_secret = fake.pystr()


class PaypalInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaypalInfo

    access_token = factory.LazyAttribute(lambda _: fake.uuid4())
    access_type = "Bearer"
    app_id = factory.LazyAttribute(lambda _: fake.uuid4())
    expires_in = "3600"
    nonce = factory.LazyAttribute(lambda _: fake.uuid4())

    @factory.post_generation
    def scopes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for scope in extracted:
                self.scopes.add(scope)
