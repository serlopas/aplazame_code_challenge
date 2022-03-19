import decimal

from django.db import transaction

from wallets import models as wallets_models
from wallets.exceptions import NotEnoughMoneyException


def top_up(
    wallet: wallets_models.Wallet,
    amount: decimal.Decimal,
) -> bool:
    with transaction.atomic():
        wallet.balance += amount
        wallet.save(update_fields=('balance', ))

    return True


def charge(
    wallet_from: wallets_models.Wallet,
    wallet_to: wallets_models.Wallet,
    amount: decimal.Decimal,
) -> bool:
    with transaction.atomic():
        customer_wallet = wallets_models.Wallet.objects\
            .select_for_update()\
            .get(pk=wallet_from.pk)
        commerce_wallet = wallets_models.Wallet.objects\
            .select_for_update()\
            .get(pk=wallet_to.pk)

        if customer_wallet.balance < amount:
            raise NotEnoughMoneyException()

        customer_wallet.balance -= amount
        commerce_wallet.balance += amount

        customer_wallet.save(update_fields=('balance', ))
        commerce_wallet.save(update_fields=('balance', ))

    return True
