from django.conf import settings as django_settings
from django.utils.module_loading import import_string
from django.utils.functional import LazyObject
from django.test.signals import setting_changed


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
    "SERIALIZERS": ObjDict(
        {
            "scope_serializer": "djpaypal.djpay.serializers.ScopeSerializer",
            "paypal_token_serializers": "djpaypal.djpay.serializers.PaypalTokenSerializer",
            "paypal_info_serializers": "djpaypal.djpay.serializers.PaypalInfoSerializer",
        }
    ),
    "PERMISSIONS": ObjDict(
        {"is_authenticated": ["rest_framework.permissions.IsAuthenticated"]}
    ),
    "AUTHENTICATION": ObjDict(
        {"basic_authentication": ["rest_framework.authentication.BasicAuthentication"]}
    ),
}


class Settings:
    # Trying to set explicit overriden settings
    def __init__(self, default_settings, explicit_overriden_settings: dict = None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        # get overriden setting form default django settings
        overriden_settings = (
            getattr(django_settings, DJPAY_SETTINGS_NAMESPACE, {})
            or explicit_overriden_settings
        )
        self._load_default_settings()
        self._override_settings(overriden_settings)

    def _load_default_settings(self):

        """
        Load default settings into object attributes.

        Sets object attributes using values from 'default_settings'.
        Only applies to settings with uppercase names.

        """
        for setting_name, setting_value in default_settings.items():
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)

    def _override_settings(self, overridden_settings: dict):

        """
        Override object settings using provided dictionary.

        Updates object attributes with settings from 'overridden_settings'.
        If a setting is a dictionary, merges it with existing attribute
        using custom `ObjDict`.

        :param overridden_settings: Dictionary of settings to apply.
        """
        for setting_name, settings_value in overridden_settings.items():
            value = settings_value

            if isinstance(settings_value, dict):
                print("Overrided Settings: ", setting_name, settings_value)
                value = getattr(self, setting_name, {})

                value.update(ObjDict(settings_value))

            setattr(self, setting_name, value)


class LazySettings(LazyObject):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = Settings(default_settings, explicit_overriden_settings)


settings = LazySettings()


def reload_djpaypal_settings(*args, **kwargs):
    global settings
    print("Settings Changed...")
    setting, value = kwargs["setting"], kwargs["value"]

    if setting == DJPAY_SETTINGS_NAMESPACE:
        settings._setup(explicit_overriden_settings=value)


setting_changed.connect(reload_djpaypal_settings)
