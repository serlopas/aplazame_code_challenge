from django.test import TestCase
from faker import Faker

from wallets import factories as wallets_factories
from wallets import services
from wallets.exceptions import NotEnoughMoneyException


class TestTopUpOperation(TestCase):

    def test_top_up(self):
        balance = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=0.0
        )
        amount = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=0.0,
            max_value=int(balance)
        )
        wallet = wallets_factories.WalletFactory(balance=balance)

        services.top_up(wallet.id, amount)

        wallet.refresh_from_db()
        self.assertEqual(wallet.balance, balance + amount)


class TestChargeOperation(TestCase):

    def test_charge(self):
        balance_from = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=0.0
        )
        balance_to = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=0.0
        )
        amount = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=0.0,
            max_value=int(balance_from)
        )
        wallet_from = wallets_factories.WalletFactory(balance=balance_from)
        wallet_to = wallets_factories.WalletFactory(balance=balance_to)

        services.charge(wallet_from.id, wallet_to.id, amount)

        wallet_from.refresh_from_db()
        wallet_to.refresh_from_db()
        self.assertEqual(wallet_from.balance, balance_from - amount)
        self.assertEqual(wallet_to.balance, balance_to + amount)

    def test_charge_not_enough_money(self):
        balance_from = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=0.0
        )
        balance_to = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=0.0
        )
        amount = Faker().pydecimal(
            left_digits=5,
            right_digits=2,
            min_value=int(balance_from) + 1,
        )
        wallet_from = wallets_factories.WalletFactory(balance=balance_from)
        wallet_to = wallets_factories.WalletFactory(balance=balance_to)

        self.assertRaises(
            NotEnoughMoneyException,
            services.charge, wallet_from.id, wallet_to.id, amount
        )
