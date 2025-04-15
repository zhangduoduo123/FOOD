from django.db import models

# Create your models here.
# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 用户名
    # 密码

    lab = models.CharField(max_length=15, blank=True)   # 实验室

    def __str__(self):
        return self.username