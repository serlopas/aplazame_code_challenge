import factory
import pytz
from factory import fuzzy

from users import models
from users import settings as users_settings


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', users_settings.USER_PASSWORD_TEST)
    last_login = factory.Faker('date_time_between', start_date='-1y', tzinfo=pytz.UTC)
    user_type = fuzzy.FuzzyChoice([user_type for user_type, _ in models.User.USER_TYPES])

    class Params:
        is_customer = factory.Trait(
            user_type=models.User.CUSTOMER
        )
        is_commerce = factory.Trait(
            user_type=models.User.COMMERCE
        )

    class Meta:
        model = models.User
