from django.conf import settings as django_settings
from django.utils.module_loading import import_string


DJPAY_SETTINGS_NAMESPACE = "DJ_PAYPAL"


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

        # get overriden setting form default django settings
        overriden_settings = (
            getattr(django_settings,DJPAY_SETTINGS_NAMESPACE,{})
            or explicit_overriden_settings
        )
        self._load_default_settings()
        self._override_settings(overriden_settings)
        # self.get_overrid(overriden_settings)

    def get_overrid(self,overriden_settings):
        print(overriden_settings)
    
    def _load_default_settings(self):
        # load default settings
        for setting_name,setting_value in default_settings.items():
            if setting_name.isupper():
                setattr(self,setting_name,setting_value)


    def _override_settings(self,overriden_settings:dict):
        """
        get overriden settings from django defaul settings
        """
        for setting_name, settings_value in overriden_settings.items():
            value = settings_value
            
            if isinstance(settings_value, dict):
                value = getattr(self,setting_name,{})
                value.update(ObjDict(settings_value))
            setattr(self,setting_name,value)

            



