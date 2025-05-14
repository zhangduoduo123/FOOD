from django.db import models
from django.contrib.auth.models import User


class UserBasicInfo(models.Model):
    uid = models.OneToOneField('UserInfo', models.DO_NOTHING, db_column='uid', primary_key=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    physical_activity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_basic_info'


class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'
