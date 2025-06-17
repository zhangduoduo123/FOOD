from django.db import models
from django.contrib.auth.models import User


class UserBasicInfo(models.Model):
    uid = models.OneToOneField('UserInfo', models.DO_NOTHING, db_column='uid', primary_key=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    physical_activity = models.CharField(max_length=255, blank=True, null=True)
    diabetes = models.CharField(max_length=255, blank=True, null=True)
    ethnicity = models.CharField(db_column='Ethnicity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vegetarian = models.CharField(db_column='Vegetarian', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_basic_info'



class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'

        # INSERT_YOUR_CODE
class MealRecommend(models.Model):
    uid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='uid')
    meal = models.CharField(max_length=100)
    adjust_info = models.CharField(max_length=200, blank=True, null=True)
    food_recommend = models.CharField(max_length=200)
    last_use_timestamp = models.DateTimeField(blank=True, null=True)
    能量_千卡 = models.BigIntegerField(db_column='能量-千卡', blank=True, null=True)
    蛋白质_克 = models.BigIntegerField(db_column='蛋白质-克', blank=True, null=True)
    脂肪_克 = models.TextField(db_column='脂肪-克', blank=True, null=True)
    碳水化合物_克 = models.TextField(db_column='碳水化合物-克', blank=True, null=True)
    钙_毫克 = models.BigIntegerField(db_column='钙-毫克', blank=True, null=True)
    磷_毫克 = models.BigIntegerField(db_column='磷-毫克', blank=True, null=True)
    钾_毫克 = models.BigIntegerField(db_column='钾-毫克', blank=True, null=True)
    钠_毫克 = models.BigIntegerField(db_column='钠-毫克', blank=True, null=True)
    镁_毫克 = models.BigIntegerField(db_column='镁-毫克', blank=True, null=True)
    铁_毫克 = models.FloatField(db_column='铁-毫克', blank=True, null=True)
    锌_毫克 = models.FloatField(db_column='锌-毫克', blank=True, null=True)
    硒_微克 = models.BigIntegerField(db_column='硒-微克', blank=True, null=True)
    碘_微克 = models.BigIntegerField(db_column='碘-微克', blank=True, null=True)
    铜_毫克 = models.FloatField(db_column='铜-毫克', blank=True, null=True)
    氟_毫克 = models.FloatField(db_column='氟-毫克', blank=True, null=True)
    铬_微克 = models.BigIntegerField(db_column='铬-微克', blank=True, null=True)
    锰_毫克 = models.FloatField(db_column='锰-毫克', blank=True, null=True)
    钼_微克 = models.BigIntegerField(db_column='钼-微克', blank=True, null=True)
    维生素A_微克 = models.BigIntegerField(db_column='维生素A-微克', blank=True, null=True)
    维生素C_毫克 = models.BigIntegerField(db_column='维生素C-毫克', blank=True, null=True)
    维生素D_微克 = models.BigIntegerField(db_column='维生素D-微克', blank=True, null=True)
    维生素E_毫克 = models.BigIntegerField(db_column='维生素E-毫克', blank=True, null=True)
    维生素K_微克 = models.BigIntegerField(db_column='维生素K-微克', blank=True, null=True)
    维生素B1_毫克 = models.FloatField(db_column='维生素B1-毫克', blank=True, null=True)
    维生素B2_毫克 = models.FloatField(db_column='维生素B2-毫克', blank=True, null=True)
    维生素B6_毫克 = models.FloatField(db_column='维生素B6-毫克', blank=True, null=True)
    维生素B12_微克 = models.FloatField(db_column='维生素B12-微克', blank=True, null=True)
    泛酸_毫克 = models.FloatField(db_column='泛酸-毫克', blank=True, null=True)
    叶酸_微克 = models.BigIntegerField(db_column='叶酸-微克', blank=True, null=True)
    烟酸_毫克 = models.BigIntegerField(db_column='烟酸-毫克', blank=True, null=True)
    生物素_微克 = models.BigIntegerField(db_column='生物素-微克', blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'meal_recommend'

