from django.db import models
from django.contrib.auth.models import User
from .managers import UserModelManager

# Create your models here.
class UserModel(models.Model):
    objects = UserModelManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class TransactionGroup(models.Model):
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="transaction_sender")
    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="transaction_receiver")
    amount = models.FloatField()
    is_paid = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)