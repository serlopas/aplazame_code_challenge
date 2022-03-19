from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(
        choices=User.USER_TYPES,
    )

    def create(self, validated_data: dict) -> User:
        validated_data['username'] = validated_data['email']

        return super().create(validated_data)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'password',
            'user_type',
        )
        read_only_fields = (
            'id',
        )
