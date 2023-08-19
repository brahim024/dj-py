import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from djpaypal.djpay.views import GenerateTokenViewSet
from djpaypal.djpay.models import PaypalInfo

@pytest.mark.skip
def test_list_access_api_without_authentication():
    """
        tests that test authentication endpont without pass authentication
    """
    client = Client()
    client_url = reverse("djpay:token-list")
    response = client.get(path=client_url)
    assert response.status_code == 401


@pytest.mark.skip(reason="Because I cant find djpay:token-get url")
@pytest.mark.django_db
def test_generate_access_token_list(user_factory, factory, paypal_token):
    request = factory.get(reverse('djpay:token-list'))
    force_authenticate(request, user=user_factory.create())
    view = GenerateTokenViewSet.as_view({'get':'list'})
    response = view(request)

    assert response.status_code == 200
    # assert response.data["client_id"] == paypal_token.client_id

# @pytest.mark.skip
@pytest.mark.django_db
def test_generate_access_token_without_auth(user_factory, factory):
    """
        test GenerateTokenViewSet wihout login
    """
    request = factory.get(reverse("djpay:token-list"))
    user = User.objects.create(username='test',password='test')

    view = GenerateTokenViewSet.as_view({'get':'list'})
    response = view(request)
    assert response.status_code == 401

# need to fix
@pytest.mark.skip
@pytest.mark.django_db
def test_generate_access_token_post_with_unvalid_credentials(
    user_factory, factory, view_post, paypal_token
    ):
    assert PaypalInfo.objects.all().count() == 0
    request = factory.post(reverse("djpay:token-post"))
    force_authenticate(request, user=user_factory.create())
    response = view_post(request)
    assert PaypalInfo.objects.all().count() == 0