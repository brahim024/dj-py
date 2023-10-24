from django.apps import AppConfig
from django.conf import settings
from django.core.signals import setting_changed
from django.dispatch import receiver


@receiver(setting_changed)
def my_callback(sender, **kwargs):
    print("Setting changed!")


class DjpayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = None
    if not hasattr(settings.DJ_PAYPAL, "PACKABLE") or settings.DJ_PAYPAL.PACKABLE:
        name = "djpaypal.djpay"
    else:
        name = "djpay"
