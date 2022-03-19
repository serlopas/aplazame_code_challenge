from django.test import TestCase
from rest_framework.fields import DecimalField, DateTimeField

from operations import factories
from operations.api.v1 import serializers


class TestOperationsSerializer(TestCase):

    def test_serializer(self):
        operation = factories.OperationFactory()

        expected_result = {
            'operation_type': operation.operation_type,
            'amount': DecimalField(
                max_digits=20, decimal_places=2
            ).to_representation(operation.amount),
            'wallet_from': operation.wallet_from.token.hex,
            'wallet_to': operation.wallet_to.token.hex,
            'success': operation.success,
            'created': DateTimeField().to_representation(operation.created),
        }
        serialized_data = serializers.OperationsSerializer(instance=operation).data

        self.assertDictEqual(serialized_data, expected_result, serialized_data)
