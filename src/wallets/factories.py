import factory

from wallets import models


class WalletFactory(factory.django.DjangoModelFactory):
    balance = factory.Faker('pydecimal', right_digits=2, min_value=0, max_value=1000)
    user = factory.SubFactory('users.factories.UserFactory')

    class Meta:
        model = models.Wallet
