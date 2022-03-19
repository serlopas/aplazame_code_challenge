from rest_framework import permissions, generics

from operations import models
from operations.api.v1 import serializers


class OperationsView(generics.ListAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.OperationsSerializer

    def get_queryset(self):
        if self.request.user.is_commerce:
            return models.Operations.objects.filter(wallet_to__user=self.request.user)

        return models.Operations.objects.filter(wallet_from__user=self.request.user)
