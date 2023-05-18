import factory
from djpaypal.djpay.models import Scope, PaypalToken, PaypalInfo
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

class PaypalInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaypalInfo
    access_token = factory.Faker('access_token')
    access_type = factory.Faker('access_type')
    app_id = factory.Faker('app_id')
    expires_in = factory.Faker('expires_in')
    nonce = factory.Faker('nonce')
    @factory.post_generation
    def scoupes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for scope in scoupes:
                self.groups.add(scoupe)