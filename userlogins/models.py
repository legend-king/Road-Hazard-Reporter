from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Authority(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authority')
    name = models.CharField(max_length=255)