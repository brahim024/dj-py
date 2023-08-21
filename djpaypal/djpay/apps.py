from django.apps import AppConfig
from django.conf import settings


class DjpayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = None
    if not hasattr(settings, 'PACKABLE') or settings.PACKABLE:
        name = 'djpay'
    else:
        name = 'djpaypal.djpay'  


