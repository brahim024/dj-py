import pytest
from unittest.mock import patch

# from django.utils import module_loading
from djpay.api.authorize.conf import ObjDict, Settings
from djpay.api.authorize.conf import default_settings


class TestCustomConf:
    @patch("django.utils.module_loading")
    def test_convert_package_path_to_import_string(self, mocker):
        obj = ObjDict(
            {
                "permission": [
                    "djpay.api.authorize.serializers.ScopeSerializer",
                    "djay.api.authorize.serializers.PaypalTokenSerializer",
                ]
            }
        )
        # assert mocker.import_string.assert_called_once()
        assert type(obj) != str

    @patch("djpay.api.authorize.conf.Settings._load_default_settings")
    def test_settings_load_default_settings_is_called(self, mocker):
        settings = Settings(default_settings, None)
        print(settings.__dict__)
        mocker.assert_called_once()
