from djpaypal.djpay.models import Scope, PaypalToken, PaypalInfo
from django.conf import settings
from django.contrib.auth.models import User
import pytest

from unittest.mock import MagicMock, patch


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
    def test_payal_info_factory_created(self, paypal_info_factory, scope_factory):
        assert PaypalInfo.objects.all().count() == 0

        s1 = scope_factory.create()
        s2 = scope_factory.create()
        user = User.objects.create()
        paypal_info = paypal_info_factory.create(user=user, scope=[s1, s2])
        assert PaypalInfo.objects.all().count() == 1
        assert paypal_info.scope.all().count() == 2
        assert PaypalInfo.objects.get(id=1).access_token == \
            paypal_info.access_token

    @pytest.mark.django_db
    def test_paypal_info_factory_representing(self, paypal_info_factory):
        pay_info = paypal_info_factory.create()
        assert str(pay_info) == pay_info.access_token

    @pytest.mark.django_db
    def test_paypal_info_return_production_paypal_link(self, paypal_info_factory):
        paypal_info = paypal_info_factory.create()
        settings.LIVE_MODE = True
        assert paypal_info.get_link_base() == "https://api.paypal.com"

    @pytest.mark.django_db
    def test_paypal_info_return_production_sandbox_link(self, paypal_info_factory):
        paypal_info = paypal_info_factory.create()
        settings.LIVE_MODE = False
        assert paypal_info.get_link_base() == "https://api.sandbox.paypal.com"

    @pytest.mark.django_db
    @patch('djpaypal.djpay.models.requests.post')
    def test_paypal_info_has_valid_extention(self, mocker, paypal_token_factory):
        mock_reponse = MagicMock(status_code=200)
        mocker.return_value = mock_reponse

        info = paypal_token_factory.create()
        has_valid = info.has_valid_token()
        assert has_valid == True

    @pytest.mark.django_db
    @patch('djpaypal.djpay.models.requests.post')
    def test_paypal_info_has_no_valid_extention(self, mocker, paypal_token_factory):
        mock_reponse = MagicMock(status_code=402)
        mocker.return_value = mock_reponse

        info = paypal_token_factory.create()
        has_valid = info.has_valid_token()
        assert has_valid == False



