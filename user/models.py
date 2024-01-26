from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid

class AccessTokenManager(models.Manager):
    def create(self, **kwargs):
        token = self.model(token=uuid.uuid4(), **kwargs)
        token.save()
        return token

class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    used = models.BooleanField(default=False)

    objects = AccessTokenManager()
