from djpay.api.authorize.conf import settings
from colored import stylize
import colored


# Define a class for PayPal URLs
class PayPalUrls:
    
    # Set the base URL for PayPal API
    BASE_URL = "https://api-m.sandbox.paypal.com"

    @classmethod
    def base_url(cls):
        """
        Get the base URL for PayPal API based on the current mode.
        """
        # if settings.LIVE_MODE == None:
        #     print(colored("Warning: your Apllying to paypal test mode"))
        #     return cls.BASE_URL
        
        cls.BASE_URL = "https://api.paypal.com" if settings.LIVE_MODE else cls.BASE_URL
        return cls.BASE_URL

    

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
