from djoser.serializers import UserCreateSerializer
from accounts import models as accounts_models


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = accounts_models.User
        fields = ('id', 'username', 'password')
