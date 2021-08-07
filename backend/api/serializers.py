from .models import UserModel
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    password = serializers.CharField(write_only=True, source='user.password')
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'discord_id', 'password')

    def create(self, validated_data):
        print(validated_data)
        user: UserModel = UserModel.objects.create_user(
            username=validated_data['user']['username'],
            first_name=validated_data['user']['first_name'],
            password=validated_data['user']['password'],
            discord_id=validated_data['discord_id']
        )
        return user