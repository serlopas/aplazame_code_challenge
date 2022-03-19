from rest_framework import serializers

from operations import models


class OperationsSerializer(serializers.ModelSerializer):
    wallet_from = serializers.CharField(source='wallet_from.token.hex')
    wallet_to = serializers.CharField(source='wallet_to.token.hex')

    class Meta:
        model = models.Operations
        fields = (
            'operation_type', 'amount', 'wallet_from', 'wallet_to', 'success',
            'created',
        )
        read_only_fields = (
            'operation_type', 'amount', 'wallet_from', 'wallet_to', 'success',
            'created',
        )
