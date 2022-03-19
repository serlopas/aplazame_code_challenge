from django.test import TestCase
from rest_framework.fields import DecimalField

from wallets import factories
from wallets.api.v1.serializers import wallets_serializers


class TestWalletSerializer(TestCase):

    def test_serializer(self):
        wallet = factories.WalletFactory()

        expected_result = {
            'token': wallet.token.hex,
            'balance': DecimalField(
                max_digits=20, decimal_places=2
            ).to_representation(wallet.balance),
        }
        serialized_data = wallets_serializers.WalletSerializer(instance=wallet).data

        self.assertDictEqual(serialized_data, expected_result, serialized_data)
