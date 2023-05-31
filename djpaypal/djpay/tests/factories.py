import factory
from djpaypal.djpay.models import Scope, PaypalToken, PaypalInfo
from faker import Faker
from django.contrib.auth.models import User


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "password")


class ScopeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Scope

    name = factory.Sequence(lambda n: f"Scope {n}")


class PaypalTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaypalToken

    app_name = fake.domain_name()
    client_id = factory.LazyAttribute(lambda _: fake.uuid4())
    client_secret = factory.LazyAttribute(lambda _: fake.uuid4())


class PaypalInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaypalInfo

    user = factory.SubFactory(UserFactory)
    tokens = factory.SubFactory(PaypalTokenFactory)
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
