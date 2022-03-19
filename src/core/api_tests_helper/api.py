import json

from django.urls import reverse
from exam import fixture
from rest_framework.test import APITestCase, APIClient

from users import factories as users_factories
from users import models as users_models
from users import settings as users_settings
from wallets import factories as wallets_factories


class BaseViewTest(APITestCase):

    @fixture
    def get_api_client(self):
        return APIClient()

    def _login_user(
            self,
            username: str,
            password: str
    ) -> APIClient:
        client = self.get_api_client
        response = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps({
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )
        token = response.data['access']
        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        client.login(username=username, password=password)

        return client

    @fixture
    def get_customer(self) -> users_models.User:
        return users_factories.UserFactory(is_customer=True)

    @fixture
    def get_customer_with_wallet(self) -> users_models.User:
        user = users_factories.UserFactory(is_customer=True)
        wallets_factories.WalletFactory(user=user)
        return user

    @fixture
    def get_commerce(self) -> users_models.User:
        return users_factories.UserFactory(is_commerce=True)

    @fixture
    def get_commerce_with_wallet(self) -> users_models.User:
        user = users_factories.UserFactory(is_commerce=True)
        wallets_factories.WalletFactory(user=user)
        return user

    @fixture
    def get_signed_customer(self):
        user = self.get_customer
        return self._login_user(
            user.username,
            users_settings.USER_PASSWORD_TEST
        )

    @fixture
    def get_signed_customer_with_wallet(self):
        user = self.get_customer_with_wallet
        return self._login_user(
            user.username,
            users_settings.USER_PASSWORD_TEST
        )

    @fixture
    def get_signed_commerce(self):
        user = self.get_commerce
        return self._login_user(
            user.username,
            users_settings.USER_PASSWORD_TEST
        )

    @fixture
    def get_signed_commerce_with_wallet(self):
        user = self.get_commerce_with_wallet
        return self._login_user(
            user.username,
            users_settings.USER_PASSWORD_TEST
        )
