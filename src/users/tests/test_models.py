from django.test import TestCase

from users import factories


class TestUsers(TestCase):

    def test_is_customer(self):
        user = factories.UserFactory(is_customer=True)

        self.assertTrue(user.is_customer)
        self.assertFalse(user.is_commerce)

    def test_is_commerce(self):
        user = factories.UserFactory(is_commerce=True)

        self.assertTrue(user.is_commerce)
        self.assertFalse(user.is_customer)
