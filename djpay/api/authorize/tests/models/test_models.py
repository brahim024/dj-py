from djpay.api.authorize.models import Scope, PaypalToken, PaypalInfo
from djpay.api.authorize.conf import settings
from django.contrib.auth.models import User
import pytest

from unittest.mock import MagicMock, patch
from djpay.api.authorize.path import PayPalUrls


class TestModels:
    @pytest.mark.django_db
    def test_scope_factory_create(self, scope_factory):
        scope_factory.create()
        assert Scope.objects.all().count() == 1

    @pytest.mark.django_db
    def test_scope_representation(self):
        scope = Scope.objects.create(name="test")

        assert str(scope) == "test"

    @pytest.mark.django_db
    def test_paypal_token_create(self, paypal_token_factory):
        assert PaypalToken.objects.all().count() == 0
        paypal_token_factory.create()
        assert PaypalToken.objects.all().count() == 1

    @pytest.mark.django_db
    def test_paypal_token_representing(self, paypal_token_factory):
        py_token = paypal_token_factory.create()
        assert str(py_token) == py_token.app_name

    @pytest.mark.django_db
    def test_paypal_info_factory_created(
        self, paypal_info_factory, scope_factory
    ):
        assert PaypalInfo.objects.all().count() == 0

        s1 = scope_factory.create()
        s2 = scope_factory.create()
        user = User.objects.create()
        paypal_info = paypal_info_factory.create(user=user, scope=[s1, s2])
        print(paypal_info_factory)
        assert PaypalInfo.objects.all().count() == 1
        assert paypal_info.scope.all().count() == 2
        assert (
            PaypalInfo.objects.get(id=str(paypal_info.id)).access_token
            == paypal_info.access_token
        )

    @pytest.mark.django_db
    def test_paypal_info_factory_representing(self, paypal_info_factory):
        pay_info = paypal_info_factory.create()
        assert str(pay_info) == pay_info.access_token

    
    def test_paypal_info_return_production_paypal_link(self):
        
        settings.LIVE_MODE = True
        print(PayPalUrls().base_url)
        assert PayPalUrls.base_url() == "https://api.paypal.com"
        settings.LIVE_MODE = False

    
    def test_paypal_info_return_sandbox_link(self):
        print(settings.LIVE_MODE)
        assert PayPalUrls.base_url() == "https://api-m.sandbox.paypal.com"


    @pytest.mark.django_db
    @patch("djpay.api.authorize.models.requests.get")
    def test_paypal_info_has_valid_extention(
        self, mocker, paypal_token_factory
    ):
        mock_reponse = MagicMock(status_code=200)
        mocker.return_value = mock_reponse

        info = paypal_token_factory.create()
        has_valid = info.has_valid_token()
        mocker.assert_called_once()
        assert has_valid == True

    @pytest.mark.django_db
    @patch("djpay.api.authorize.models.requests.post")
    def test_paypal_info_has_no_valid_extention(
        self, mocker, paypal_token_factory
    ):
        mock_reponse = MagicMock(status_code=402)
        mocker.return_value = mock_reponse

        info = paypal_token_factory.create()
        has_valid = info.has_valid_token()
        assert has_valid == False
