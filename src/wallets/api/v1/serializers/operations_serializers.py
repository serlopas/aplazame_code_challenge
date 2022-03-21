from rest_framework import serializers

from operations import models
from wallets import services
from wallets.exceptions import NotEnoughMoneyException
from wallets import models as wallets_models


class OperationsTopUpSerializer(serializers.ModelSerializer):
    wallet_from = serializers.CharField(source='wallet_from.token.hex', read_only=True)

    def create(self, validated_data: dict) -> models.Operations:
        wallet = self.context['wallet']
        validated_data['success'] = services.top_up(wallet.id, validated_data['amount'])
        validated_data['wallet_from'] = wallet
        validated_data['operation_type'] = models.Operations.TOPUP

        return super().create(validated_data)

    class Meta:
        model = models.Operations
        fields = (
            'operation_type', 'amount', 'wallet_from', 'success', 'created',
        )
        read_only_fields = (
            'operation_type', 'wallet_from', 'success', 'created',
        )


class OperationsChargeSerializer(serializers.ModelSerializer):
    wallet = serializers.CharField(write_only=True)
    wallet_from = serializers.CharField(source='wallet_from.token.hex', read_only=True)
    wallet_to = serializers.CharField(source='wallet_to.token.hex', read_only=True)

    def create(self, validated_data: dict) -> models.Operations:
        wallet_to = self.context['wallet']
        wallet_from = wallets_models.Wallet.objects.get(token=validated_data.pop('wallet'))
        try:
            validated_data['success'] = services.charge(
                wallet_from_id=wallet_from.id,
                wallet_to_id=wallet_to.id,
                amount=validated_data['amount'],
            )
        except NotEnoughMoneyException as e:
            validated_data['success'] = False
            validated_data['error_reason'] = str(e)

        validated_data['wallet_to'] = wallet_to
        validated_data['wallet_from'] = wallet_from
        validated_data['operation_type'] = models.Operations.CHARGE

        return super().create(validated_data)

    class Meta:
        model = models.Operations
        fields = (
            'operation_type', 'amount', 'wallet_from', 'wallet_to', 'success',
            'created', 'wallet',
        )
        read_only_fields = (
            'operation_type', 'wallet_from', 'wallet_to', 'success', 'created',
        )
        extra_kwargs = {
            'amount': {'write_only': True},
        }
