import uuid as uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Wallet(TimeStampedModel):

    token = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.0,
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='wallets'
    )
