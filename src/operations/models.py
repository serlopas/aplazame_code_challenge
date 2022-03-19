from django.db import models
from django_extensions.db.models import TimeStampedModel

from wallets import models as wallets_models


class Operations(TimeStampedModel):
    TOPUP = 'Top-up'
    CHARGE = 'Charge'

    OPERATION_TYPES = (
        (TOPUP, TOPUP),
        (CHARGE, CHARGE),
    )

    operation_type = models.CharField(
        choices=OPERATION_TYPES,
        max_length=16,
        db_index=True,
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.0,
    )
    wallet_from = models.ForeignKey(
        wallets_models.Wallet,
        on_delete=models.DO_NOTHING,
        related_name='operations_from',
    )
    wallet_to = models.ForeignKey(
        wallets_models.Wallet,
        on_delete=models.DO_NOTHING,
        related_name='operations_to',
        null=True,
    )
    success = models.BooleanField()
    error_reason = models.CharField(
        max_length=256,
    )
