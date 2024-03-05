from djpay.api.authorize.models import PaypalInfo, PaypalToken
from djpay.api.authorize.conf import settings


def get_paypal_token():
    """
    Retrieve the PaypalToken object associated with the app name.
    """
    
    return PaypalToken.objects.get(app_name=settings.PAYPAL_TOKEN_APP_NAME)
    