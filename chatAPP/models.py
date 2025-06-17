# chatAPP/models.py
from django.db import models

class Conservation(models.Model):
    conservation_id = models.AutoField(primary_key=True)
    conservation_title = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    uid = models.ForeignKey('UserApp.UserInfo', models.CASCADE, db_column='uid', blank=True, null=True)

    class Meta:
        managed = True  # 设置为 True，让 Django 管理这个表
        db_table = 'conservation'

class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    conservation = models.ForeignKey(Conservation, models.CASCADE)
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'content'