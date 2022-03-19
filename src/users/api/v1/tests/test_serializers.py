import random

from django.test import TestCase
from faker import Faker

from users.api.v1 import serializers
from users.models import User


class TestCommerceSerializer(TestCase):

    def test_serializer(self):
        data = {
            'email': Faker().email(),
            'first_name': Faker().first_name(),
            'last_name': Faker().last_name(),
            'password': Faker().password(),
            'user_type': random.choice([user_type for user_type, _ in User.USER_TYPES]),
        }

        user = serializers.UserSerializer().create(validated_data=data)

        self.assertTrue(
            all(getattr(user, field) == data[field] for field in data.keys())
        )
        self.assertEqual(user.username, data['email'])
