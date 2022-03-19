import factory
from factory import fuzzy

from operations import models as operations_models
from users import models as users_models


class OperationFactory(factory.django.DjangoModelFactory):

    operation_type = fuzzy.FuzzyChoice(
        [user_type for user_type, _ in operations_models.Operations.OPERATION_TYPES]
    )
    amount = factory.Faker('pydecimal', right_digits=2, min_value=0, max_value=1000)
    wallet_from = factory.SubFactory(
        'wallets.factories.WalletFactory',
        user__user_type=users_models.User.CUSTOMER
    )
    wallet_to = factory.SubFactory(
        'wallets.factories.WalletFactory',
        user__user_type=users_models.User.COMMERCE
    )
    success = factory.Faker('pybool')

    class Meta:
        model = operations_models.Operations
