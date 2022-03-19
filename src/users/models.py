from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CUSTOMER, COMMERCE = 'Customer', 'Commerce'

    USER_TYPES = (
        (CUSTOMER, CUSTOMER),
        (COMMERCE, COMMERCE),
    )

    user_type = models.CharField(
        max_length=16,
        db_index=True,
        choices=USER_TYPES,
    )

    @property
    def is_customer(self):
        return self.user_type == self.CUSTOMER

    @property
    def is_commerce(self):
        return self.user_type == self.COMMERCE
