from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserModel(User):
    discord_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class TransactionGroup(models.Model):
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    is_paid = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)