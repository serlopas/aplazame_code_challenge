import random

from django.urls import reverse
from faker import Faker
from rest_framework import status

from core.api_tests_helper.api import BaseViewTest
from users import models


class TestUsersView(BaseViewTest):

    @property
    def endpoint(self):
        return reverse('users:v1:users')

    def test_method_not_allowed(self):
        for method in ('get', 'put', 'patch', 'delete'):
            with self.subTest(method):
                response = getattr(self.get_api_client, method)(self.endpoint)

                self.assertEqual(
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    response.status_code,
                    response.content
                )

    def test_create_user(self):
        data = {
            'email': Faker().email(),
            'first_name': Faker().first_name(),
            'last_name': Faker().last_name(),
            'password': Faker().password(),
            'user_type': random.choice([user_type for user_type, _ in models.User.USER_TYPES]),
        }

        response = self.get_api_client.post(self.endpoint, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.content
        )
        self.assertTrue(models.User.objects.filter(email=data['email']).exists())
