from django.apps import AppConfig
from django.core.signals import setting_changed
from django.dispatch import receiver


@receiver(setting_changed)
def my_callback(sender, **kwargs):
    print("Setting changed!")


class SubscriptionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "djpay.api.subscriptions"
    # label = "paypal_authentication"
