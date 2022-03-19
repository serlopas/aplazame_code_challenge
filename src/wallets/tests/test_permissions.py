from django.test import TestCase
from rest_framework.permissions import BasePermission
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from wallets import permissions
from wallets import factories as wallets_factories
from users import factories as users_factories
from users import models as users_models


class TestWalletsPermission(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.permission: BasePermission = permissions.WalletsPermission()
        cls.path = '/wallets'
        cls.view = APIView()

    def test_safe_methods(self):
        request = self.view.initialize_request(
            APIRequestFactory().get(path=self.path)
        )
        request.user = users_factories.UserFactory()

        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_on_creation_user_without_wallet(self):
        test_data_list = (
            # Test message              User Type
            ('Customer without wallet', users_models.User.CUSTOMER, ),
            ('Commerce without wallet', users_models.User.COMMERCE, ),
        )

        for msg, user_type in test_data_list:
            with self.subTest(msg=msg):
                request = self.view.initialize_request(
                    APIRequestFactory().post(path=self.path)
                )
                request.user = users_factories.UserFactory(user_type=user_type)

                self.assertTrue(self.permission.has_permission(request, self.view))

    def test_on_creation_user_with_wallet(self):
        test_data_list = (
            # Test message              User Type                   Expected result
            ('Customer with wallet',    users_models.User.CUSTOMER, True, ),
            ('Commerce with wallet',    users_models.User.COMMERCE, False, ),
        )

        for msg, user_type, expected_result in test_data_list:
            with self.subTest(msg=msg):
                request = self.view.initialize_request(
                    APIRequestFactory().post(path=self.path)
                )
                request.user = wallets_factories.WalletFactory(user__user_type=user_type).user

                self.assertEqual(
                    self.permission.has_permission(request, self.view),
                    expected_result
                )


class TestWalletsDetailPermission(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.permission: BasePermission = permissions.WalletsIsOwnerPermission()
        cls.path = '/wallets/uuid'
        cls.view = APIView()

    def test_permission_true(self):
        wallet = wallets_factories.WalletFactory()
        request = self.view.initialize_request(
            APIRequestFactory().get(path=self.path)
        )
        request.user = wallet.user

        self.assertTrue(
            self.permission.has_object_permission(request, self.view, wallet)
        )

    def test_permission_false(self):
        wallet = wallets_factories.WalletFactory()
        request = self.view.initialize_request(
            APIRequestFactory().get(path=self.path)
        )
        request.user = users_factories.UserFactory()

        self.assertFalse(
            self.permission.has_object_permission(request, self.view, wallet)
        )


class TestWalletsTopUpPermission(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.permission: BasePermission = permissions.WalletsTopUpPermission()
        cls.path = '/wallets/uuid/topup'
        cls.view = APIView()

    def test_permission(self):
        test_data_list = (
            # User operation_type                     # Expected result
            (users_models.User.CUSTOMER,    True, ),
            (users_models.User.COMMERCE,    False, ),
        )

        for user_type, expected_result in test_data_list:
            with self.subTest(msg=user_type):
                request = self.view.initialize_request(
                    APIRequestFactory().post(path=self.path)
                )
                request.user = users_factories.UserFactory(user_type=user_type)

                self.assertEqual(
                    self.permission.has_permission(request, self.view),
                    expected_result
                )


class TestWalletsChargePermission(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.permission: BasePermission = permissions.WalletsChargePermission()
        cls.path = '/wallets/uuid/charge'
        cls.view = APIView()

    def test_permission(self):
        test_data_list = (
            # User operation_type                     # Expected result
            (users_models.User.COMMERCE,    True, ),
            (users_models.User.CUSTOMER,    False, ),
        )

        for user_type, expected_result in test_data_list:
            with self.subTest(msg=user_type):
                request = self.view.initialize_request(
                    APIRequestFactory().post(path=self.path)
                )
                request.user = users_factories.UserFactory(user_type=user_type)

                self.assertEqual(
                    self.permission.has_permission(request, self.view),
                    expected_result
                )
