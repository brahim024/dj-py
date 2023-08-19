from djpaypal.djpay.models import Scope, PaypalToken, PaypalInfo
from django.conf import settings
from django.contrib.auth.models import User
import pytest
from unittest.mock import patch, Mock



def test_scope_factory_create(db, scope_factory):
    scope_factory.create()
    assert Scope.objects.all().count() == 1


def test_scope_representation(db):
    scope = Scope.objects.create(name="test")
    assert str(scope) == "test"


def test_paypal_token_create(db, paypal_token_factory):
    assert PaypalToken.objects.all().count() == 0
    paypal_token_factory.create()
    assert PaypalToken.objects.all().count() == 1


def test_paypal_token_representing(db, paypal_token_factory):
    py_token = paypal_token_factory.create()
    assert str(py_token) == py_token.app_name


def test_payal_info_factory_created(db, paypal_info_factory, scope_factory):
    assert PaypalInfo.objects.all().count() == 0

    s1 = scope_factory.create()
    s2 = scope_factory.create()
    user = User.objects.create()
    paypal_info = paypal_info_factory.create(user=user, scope=[s1, s2])
    assert PaypalInfo.objects.all().count() == 1
    assert paypal_info.scope.all().count() == 2
    assert PaypalInfo.objects.get(id=1).access_token == \
           paypal_info.access_token


def test_paypal_info_factory_representing(db, paypal_info_factory):
    pay_info = paypal_info_factory.create()
    assert str(pay_info) == pay_info.access_token


def test_paypal_info_return_production_paypal_link(db, paypal_info_factory):
    paypal_info = paypal_info_factory.create()
    settings.LIVE_MODE = True
    assert paypal_info.get_link_base() == "https://api.paypal.com"


def test_paypal_info_return_production_sandbox_link(db, paypal_info_factory):
    paypal_info = paypal_info_factory.create()
    settings.LIVE_MODE = False
    assert paypal_info.get_link_base() == "https://api.sandbox.paypal.com"

def test_models_representation(db,scope_factory):
    scope = scope_factory.create()
    assert scope.name == str(scope.name) 

# @pytest.mark.django_db
# def test_has_valid_token(db,paypal_token_factory,mock_get):
#     mock_response = mock_get
#     mock_response.status_code = 200

#     mock_get.return_value = mock_response

#     paypal_link = paypal_token_factory.create()
    
#     has_valid = paypal_link.has_valid_token()

#     mock_get.assert_called_once()

#     assert has_valid.status_code == 200

# @pytest.mark.skip(reason="AssertionError: Expected 'mock' to have been called once. Called 0 times.")
@pytest.mark.django_db
@patch('djpaypal.djpay.models.PaypalToken.has_valid_token')
def test_has_valid_token_invalid_response(paypal_token_factory,mock_get):
    # Create an instance of PaypalToken with dummy data
    user = User.objects.create(username='test',password='test')
    factory_paypal = PaypalToken.objects.create(app_name='test',client_id='test',client_secret='test',user=user)
    mock_get.return_value = False
    result = factory_paypal.has_valid_token()
    print(result)
    # assert result  == False 
    # token = paypal_token_factory.create()

    # mock_response = Mock()
    # mock_response.status_code = 401

    # # Configure the mock to return the mock response
    # mock_get.return_value = mock_response
    # response = token.has_valid_token()

    # # Call the method being tested
    # # mock_get.assert_called_once()
    # # Assert that the method returns False since the status_code is 401
    # assert response.return_value == False