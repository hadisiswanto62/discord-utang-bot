from .models import UserModel, Transaction, TransactionGroup
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    password = serializers.CharField(write_only=True, source='user.password')
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'discord_id', 'password')

    def create(self, validated_data):
        user: UserModel = UserModel.objects.create_user(
            username=validated_data['user']['username'],
            first_name=validated_data['user']['first_name'],
            password=validated_data['user']['password'],
            discord_id=validated_data['discord_id']
        )
        return user

class TransactionGroupSerializer(serializers.ModelSerializer):
    is_paid = serializers.BooleanField(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = TransactionGroup
        fields = ('id', 'desc', 'receiver', 'is_paid')

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is None:
            raise serializers.ValidationError('Internal error: request data is not passed to the serializer')

        return TransactionGroup.objects.create(
            desc=validated_data["desc"],
            receiver=request.user.usermodel
        )


class TransactionSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True)
    tx_group_id = serializers.IntegerField(write_only=True)
    group = TransactionGroupSerializer(read_only=True)
    is_paid = serializers.BooleanField(default=False)
    class Meta:
        model = Transaction
        fields = ('id', 'sender', 'receiver', 'sender_id', 'tx_group_id', 'amount', 'group', 'is_paid')

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is None:
            raise serializers.ValidationError('Internal error: request data is not passed to the serializer')
        elif request.user is None:
            raise serializers.ValidationError('User is not signed in!')
        elif request.user.usermodel is None:
            raise serializers.ValidationError('Internal error: User exist but UserModel does not exist!')

        usermodel: UserModel = request.user.usermodel
        receiver_id = usermodel.user.id
        sender = UserModel.objects.get(user__id=validated_data["sender_id"])
        tx_group = TransactionGroup.objects.get(id=validated_data["tx_group_id"])
        return Transaction.objects.create(
            sender = sender,
            receiver = usermodel,
            group = tx_group,
            amount = validated_data["amount"],
            is_paid = validated_data["is_paid"]
        )