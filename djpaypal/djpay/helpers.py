from djpaypal.djpay.models import PaypalInfo, PaypalToken
from djpaypal.djpay.conf import settings


def get_paypal_token():
    """
    Retrieve the PaypalToken object associated with the app name.
    """
    try:
        return PaypalToken.objects.get(app_name=settings.PAYPAL_TOKEN_APP_NAME)
    except PaypalInfo.DoesNotExist as e:
        return f"Invalid App token info or not exist: {e}"
