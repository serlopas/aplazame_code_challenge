from django.test import TestCase
from faker import Faker
from mock import mock

from wallets import factories as wallets_factories
from wallets.api.v1.serializers import operations_serializers
from operations import models as operations_models
from wallets.exceptions import NotEnoughMoneyException


class TestOperationsTopUpSerializer(TestCase):

    def test_serializer(self):
        wallet = wallets_factories.WalletFactory()
        data = {
            'amount': Faker().pydecimal(
                left_digits=5,
                right_digits=2,
                min_value=0.0,
            ),
        }

        operation = operations_serializers.OperationsTopUpSerializer(
            context={'wallet': wallet}
        ).create(validated_data=data)

        self.assertIsNotNone(operation)
        self.assertEqual(operation.operation_type, operations_models.Operations.TOPUP)
        self.assertEqual(operation.wallet_from, wallet)
        self.assertTrue(operation.success)
        self.assertTrue(operation.amount, data['amount'])


class TestOperationsChargeSerializer(TestCase):

    def setUp(self) -> None:
        self.wallet_to = wallets_factories.WalletFactory()
        self.wallet_from = wallets_factories.WalletFactory()
        self.data = {
            'amount': Faker().pydecimal(
                left_digits=5,
                right_digits=2,
                min_value=0.0,
                max_value=int(self.wallet_from.balance)
            ),
            'wallet': self.wallet_from.token,
        }

    def test_serializer(self):
        with mock.patch('wallets.services.charge', return_value=True):
            operation = operations_serializers.OperationsChargeSerializer(
                context={'wallet': self.wallet_to}
            ).create(validated_data=self.data)

            self.assertIsNotNone(operation)
            self.assertEqual(operation.operation_type, operations_models.Operations.CHARGE)
            self.assertEqual(operation.wallet_from, self.wallet_from)
            self.assertEqual(operation.wallet_to, self.wallet_to)
            self.assertTrue(operation.success)
            self.assertTrue(operation.amount, self.data['amount'])

    def test_serializer_raise_exception_service(self):
        with mock.patch('wallets.services.charge') as mock_charge:
            mock_charge.side_effect = NotEnoughMoneyException

            operation = operations_serializers.OperationsChargeSerializer(
                context={'wallet': self.wallet_to}
            ).create(validated_data=self.data)

            self.assertIsNotNone(operation)
            self.assertEqual(operation.operation_type, operations_models.Operations.CHARGE)
            self.assertEqual(operation.wallet_from, self.wallet_from)
            self.assertEqual(operation.wallet_to, self.wallet_to)
            self.assertFalse(operation.success)
            self.assertEqual(operation.error_reason, str(NotEnoughMoneyException()))
            self.assertTrue(operation.amount, self.data['amount'])
