from .models import UserModel
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'discord_id', 'password')

    def create(self, validated_data):
        user: UserModel = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            discord_id=validated_data['discord_id']
        )
        return user