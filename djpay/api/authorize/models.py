from django.db import models
import requests
from djpay.api.authorize.conf import settings as settings
from django.contrib.auth import get_user_model, update_session_auth_hash
import uuid

User = get_user_model()


class UUIDModel(models.Model):
    # Define an id field that uses UUIDField with primary_key=True, default=uuid.uuid4, and editable=False
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Define a Meta class that sets abstract=True
    class Meta:
        abstract = True


# Create your models here.
class Scope(UUIDModel):
    name = models.CharField(max_length=255)
    

    class Meta:
        app_label = "paypal_authentication"

    def __str__(self):
        return self.name


class PaypalToken(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)

    class Meta:
        app_label = "paypal_authentication"

    def __str__(self):
        return self.app_name

    def has_valid_token(self):
        base_url = PaypalInfo.get_link_base()
        url = base_url + "/v1/identity/oauth2/userinfo?schema=paypalv1.1"
        # print("URL TO CHECK: ",url)
        print(self.client_id, "  --------->  ", self.client_secret)
        body_params = {"grant_type": "client_credentials"}
        try:
            response = requests.get(
                url,
                body_params,
                auth=(self.client_id, self.client_secret),
                timeout=10,
            )
            print(response)

        except requests.exceptions.Timeout:
            return "Timed Out"
        except requests.exceptions.ConnectionError:
            return "Connection Error"
        except requests.exceptions.HTTPError:
            return "HttpError raised"
        else:
            print("Valid Token: ", response.status_code)
            return response.status_code == 200


class PaypalInfo(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scope = models.ManyToManyField(Scope)
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    expires_in = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)

    class Meta:
        app_label = "paypal_authentication"

    @classmethod
    def get_link_base(cls):
        """
        Get the base URL for PayPal API based on the current mode.
        """
        if settings.LIVE_MODE:
            return "https://api.paypal.com"
        return "https://api.sandbox.paypal.com"

    def __str__(self):
        return self.access_token
