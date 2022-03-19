from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='token.hex', required=False)

    def create(self, validated_data: dict) -> Wallet:
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Wallet
        fields = ('token', 'balance',)
        read_only_fields = ('token', 'balance', )
