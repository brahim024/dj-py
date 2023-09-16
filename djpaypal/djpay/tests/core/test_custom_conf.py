import pytest
from unittest.mock import patch

# from django.utils import module_loading
from djpaypal.djpay.conf import ObjDict


class TestCustomConf:
    @patch("django.utils.module_loading.import_string")
    def test_convert_package_path_to_import_string(self, mocker):
        obj = ObjDict({"permission": "djpay.serializers.ScopeSerializer"})
        print(mocker.call_count)
        assert type(obj) != str
