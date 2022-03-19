from django.urls import reverse
from rest_framework import status

from core.api_tests_helper.api import BaseViewTest
from operations import factories


class TestWalletsView(BaseViewTest):

    @property
    def endpoint(self):
        return reverse('operations:v1:operations')

    def test_method_not_allowed(self):
        for method in ('post', 'put', 'patch', 'delete'):
            with self.subTest(method):
                response = getattr(self.get_signed_customer, method)(self.endpoint)

                self.assertEqual(
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    response.status_code,
                    response.content
                )

    def test_get_customer_operations(self):
        factories.OperationFactory(
            wallet_from=self.get_customer_with_wallet.wallets.first(),
            wallet_to=self.get_commerce_with_wallet.wallets.first(),
        )
        factories.OperationFactory()

        test_data_list = (
            ('Customer', self.get_signed_customer_with_wallet, ),
            ('Commerse', self.get_signed_commerce_with_wallet, ),
        )

        for msg, api_client in test_data_list:
            with self.subTest(msg=msg):
                response = api_client.get(self.endpoint)

                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK,
                    response.content
                )
                self.assertEqual(len(response.json()), 1)
