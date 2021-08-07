from django.db import models
from django.contrib.auth.models import User

class UserModelManager(models.Manager):
    def create_user(self, **obj_data):
        disc_id = obj_data.pop("discord_id")
        user = User.objects.create_user(**obj_data)
        return super().create(user=user, discord_id=disc_id)