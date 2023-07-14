from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Scope(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "djpay"

    def __str__(self):
        return self.name


class PaypalToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)

    class Meta:
        app_label = "djpay"

    def __str__(self):
        return self.app_name


class PaypalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scope = models.ManyToManyField(Scope)
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    expires_in = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)

    class Meta:
        app_label = "djpay"

    @classmethod
    def get_link_base(cls):
        if settings.LIVE_MODE:
            return "https://api.paypal.com"
        return "https://api.sandbox.paypal.com"

    def __str__(self):
        return self.access_token
