from djpay.api.authorize.conf import settings
from colored import stylize


# Define a class for PayPal URLs
class PayPalUrls:
    
    # Set the base URL for PayPal API
    BASE_URL = "https://api-m.sandbox.paypal.com"

    @classmethod
    def base_url(self):
        """
        Get the base URL for PayPal API based on the current mode.
        """
        
        if settings.LIVE_MODE == True:
            return "https://api.paypal.com"
        else:
            return self.BASE_URL

    

    # Set the URL for getting access token
    AUTH = BASE_URL + "/v1/oauth2/token"

    # Set the URL for creating subscriptions
    CREATE_SUBSCRIPTION = BASE_URL + "/v1/billing/subscriptions"

    # Set the URL for managing subscriptions
    MANAGE_SUBSCRIPTION = (
        BASE_URL + "/v1/billing/subscriptions/{subscription_id}"
    )

    # Set the URL for creating plans
    CREATE_PLAN = BASE_URL + "/v1/billing/plans"
