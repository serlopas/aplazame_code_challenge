from django.urls import reverse
from faker import Faker
from rest_framework import status

from core.api_tests_helper.api import BaseViewTest


class TestWalletsView(BaseViewTest):

    @property
    def endpoint(self):
        return reverse('wallets:v1:wallets')

    def test_method_not_allowed(self):
        for method in ('put', 'patch', 'delete'):
            with self.subTest(method):
                response = getattr(self.get_signed_customer, method)(self.endpoint)

                self.assertEqual(
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    response.status_code,
                    response.content
                )

    def test_not_signed_user(self):
        response = self.get_api_client.post(self.endpoint)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            response.content
        )

    def test_create_wallet(self):
        response = self.get_signed_customer.post(self.endpoint)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.content
        )
        customer = self.get_customer
        self.assertTrue(customer.wallets.exists())

    def test_create_wallet_commerce_with_another_wallet(self):
        response = self.get_signed_commerce_with_wallet.post(self.endpoint)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.content
        )

    def test_get_wallets(self):
        response = self.get_signed_customer_with_wallet.get(self.endpoint)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.content
        )
        self.assertEqual(len(response.json()), 1)


class TestWalletsDetailView(BaseViewTest):

    def endpoint(self, token: str):
        return reverse(
            'wallets:v1:wallets_detail',
            kwargs={'token': token}
        )

    def test_method_not_allowed(self):
        wallet = self.get_customer_with_wallet.wallets.first()

        for method in ('put', 'patch', 'post', 'delete'):
            with self.subTest(method):
                response = getattr(self.get_signed_customer, method)(self.endpoint(wallet.token.hex))

                self.assertEqual(
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    response.status_code,
                    response.content
                )

    def test_wallet_detail(self):
        wallet = self.get_customer_with_wallet.wallets.first()
        response = self.get_signed_customer_with_wallet.get(self.endpoint(wallet.token.hex))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.content
        )

    def test_wallet_detail_another_user(self):
        wallet = self.get_customer_with_wallet.wallets.first()
        response = self.get_signed_commerce_with_wallet.get(self.endpoint(wallet.token.hex))

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.content
        )


class TestWalletsTopUpView(BaseViewTest):

    def endpoint(self, token: str):
        return reverse(
            'wallets:v1:wallets_top_up',
            kwargs={'token': token}
        )

    def test_method_not_allowed(self):
        wallet = self.get_customer_with_wallet.wallets.first()

        for method in ('put', 'patch', 'get', 'delete'):
            with self.subTest(method):
                response = getattr(
                    self.get_signed_customer_with_wallet, method
                )(self.endpoint(wallet.token.hex))

                self.assertEqual(
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    response.status_code,
                    response.content
                )

    def test_top_up_wallet(self):
        wallet = self.get_customer_with_wallet.wallets.first()
        data = {
            'amount': Faker().pydecimal(left_digits=5, right_digits=2, min_value=0.0)
        }

        response = self.get_signed_customer_with_wallet.post(
            self.endpoint(wallet.token.hex), data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.content
        )
        self.assertTrue(wallet.operations_from.exists())

    def test_top_up_with_commerce_user(self):
        wallet = self.get_commerce_with_wallet.wallets.first()
        data = {
            'amount': Faker().pydecimal(left_digits=5, right_digits=2, min_value=0.0)
        }

        response = self.get_signed_commerce_with_wallet.post(
            self.endpoint(wallet.token.hex), data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.content
        )


class TestWalletsChargeView(BaseViewTest):

    def endpoint(self, token: str):
        return reverse(
            'wallets:v1:wallets_charge',
            kwargs={'token': token}
        )

    def test_method_not_allowed(self):
        wallet = self.get_commerce_with_wallet.wallets.first()

        for method in ('put', 'patch', 'get', 'delete'):
            with self.subTest(method):
                response = getattr(
                    self.get_signed_commerce_with_wallet, method
                )(self.endpoint(wallet.token.hex))

                self.assertEqual(
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    response.status_code,
                    response.content
                )

    def test_charge_with_customer_user(self):
        wallet = self.get_customer_with_wallet.wallets.first()
        data = {
            'amount': Faker().pydecimal(left_digits=5, right_digits=2, min_value=0.0)
        }

        response = self.get_signed_customer_with_wallet.post(
            self.endpoint(wallet.token.hex), data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.content
        )

    def test_charge_wallet(self):
        wallet = self.get_commerce_with_wallet.wallets.first()
        customer_wallet = self.get_customer_with_wallet.wallets.first()
        data = {
            'wallet': customer_wallet.token.hex,
            'amount': Faker().pydecimal(
                left_digits=5,
                right_digits=2,
                min_value=0.0,
                max_value=int(customer_wallet.balance) + 1000,
            )
        }

        response = self.get_signed_commerce_with_wallet.post(
            self.endpoint(wallet.token.hex), data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.content
        )
        self.assertTrue(wallet.operations_to.exists())
        self.assertTrue(customer_wallet.operations_from.exists())
