from rest_framework import permissions, generics

from users.api.v1 import serializers


class UsersView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)
