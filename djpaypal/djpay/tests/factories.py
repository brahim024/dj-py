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
    access_token = faker.password(length=50, special_chars=False, upper_case=False)
    access_type = faker.random_choices(elements=('Bearer', 'Basic', 'JWT'))
    app_id = faker.md5(raw_output=False)
    expires_in = faker.date_between()
    nonce = f"{faker.date_between()}_{faker.md5(raw_output=False)}"

    @factory.post_generation
    def scoupes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for scope in scoupes:
                self.scoupes.add(scope)