from django.conf import settings as django_settings
from django.utils.module_loading import import_string


DJOSER_SETTINGS_NAMESPACE = "DJPAY"


class ObjDict(dict):
    def __getattribute__(self, item):
        try:
            val = self[item]
            if isinstance(val, str):
                val = import_string(val)
            elif isinstance(val, (list, tuple)):
                val = [import_string(v) if isinstance(v, str) else v for v in val]
            self[item] = val
        except KeyError:
            val = super().__getattribute__(item)

        return val
    

default_settings = {
    "LIVE_MODE": False,
    "SERIALIZERS":ObjDict(
        {
            "scope_serializer":"djpay.serializers.ScopeSerializer",
            "paypal_token_serializers":"djpay.serializers.PaypalTokenSerializer",
            "payal_info_serializers":"djpay.serializers.PaypalInfoSerializer",
        }
    ),
    
}


class Settings:
    # Trying to set explicit overriden settings
    def __init__(self,default_settings, explicit_overriden_settings:dict = None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        overriden_settings = (
            getattr(django_settings,DJOSER_SETTINGS_NAMESPACE,None)
            or explicit_overriden_settings
        )
        self._load_default_settings(self)

    def _load_default_settings(self):
        pass