from rest_framework import permissions, generics

from wallets import models
from wallets import permissions as wallets_permissions
from wallets.api.v1 import serializers as wallets_serializers
from operations import serializers as operations_serializers


class WalletsView(generics.ListCreateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
        wallets_permissions.WalletsPermission,
    )
    serializer_class = wallets_serializers.WalletSerializer

    def get_queryset(self):
        return models.Wallet.objects.filter(user=self.request.user)


class WalletsDetailView(generics.RetrieveAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
        wallets_permissions.WalletsIsOwnerPermission,
    )
    serializer_class = wallets_serializers.WalletSerializer
    queryset = models.Wallet.objects.all().select_related('user')
    lookup_field = 'token'


class WalletsOperationsBaseView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        wallets_permissions.WalletsIsOwnerPermission,
    )
    queryset = models.Wallet.objects.all()
    lookup_field = 'token'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['wallet'] = self.get_object()

        return context


class WalletsTopUpView(WalletsOperationsBaseView):

    permission_classes = WalletsOperationsBaseView.permission_classes + (
        wallets_permissions.WalletsTopUpPermission,
    )
    serializer_class = operations_serializers.OperationsTopUpSerializer


class WalletsChargeView(WalletsOperationsBaseView):

    permission_classes = WalletsOperationsBaseView.permission_classes + (
        wallets_permissions.WalletsChargePermission,
    )
    serializer_class = operations_serializers.OperationsChargeSerializer
