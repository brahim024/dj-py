from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Scope(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "djpay"

    def __str__(self):
        return self.name


class PaypalToken(models.Model):
    app_name = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)

    class Meta:
        app_label = "djpay"

    def __str__(self):
        return self.app_name


class PaypalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tokens = models.OneToOneField(PaypalToken, on_delete=models.CASCADE)
    scopes = models.ManyToManyField(Scope)
    access_token = models.CharField(max_length=255)
    access_type = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    expires_in = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)

    class Meta:
        app_label = "djpay"

    def __str__(self):
        return self.access_token
