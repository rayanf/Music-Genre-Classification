from django.db import models


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30,unique = True)
    password = models.CharField(max_length=30)
    avatar = models.CharField(max_length=30)
    active = models.BooleanField(default=False)
    token = models.UUIDField(null=True)
