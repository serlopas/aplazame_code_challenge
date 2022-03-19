import factory

from operations import models as operations_models
from users import models as users_models


class OperationTopUpFactory(factory.django.DjangoModelFactory):

    operation_type = operations_models.Operations.TOPUP
    amount = factory.Faker('pydecimal', right_digits=2, min_value=0, max_value=1000)
    wallet_from = factory.SubFactory(
        'wallets.factories.WalletFactory',
        user__user_type=users_models.User.CUSTOMER
    )
    success = factory.Faker('pybool')

    class Meta:
        model = operations_models.Operations


class OperationChargeFactory(OperationTopUpFactory):

    operation_type = operations_models.Operations.CHARGE
    wallet_to = factory.SubFactory(
        'wallets.factories.WalletFactory',
        user__user_type=users_models.User.COMMERCE
    )
