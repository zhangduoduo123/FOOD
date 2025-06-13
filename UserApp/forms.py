from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from UserApp.models import *

# 用户登录
class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入用户名'}
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入密码'},
        min_length=6
    )


# 用户注册
class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入用户名'}
    )
    telephone = forms.CharField(
        label="手机号",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入手机号'}
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入密码'},
        min_length=6
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请再次输入密码'}
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("两次输入的密码不一致")

        return cleaned_data

# 用户修改个人信息
class UserBasicInfoForm(forms.Form):
    height = forms.FloatField(
        label='身高（cm）',
        min_value=0,
        help_text='请输入你的身高，单位为厘米',
        error_messages={
            'required': '身高是必填项',
            'min_value': '身高不能为负数',
        },
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        label='年龄',
        min_value=0,
        max_value=100,
        help_text='请输入你的年龄',
        error_messages={
            'required': '年龄是必填项',
            'min_value': '年龄不能为负数',
            'max_value': '年龄不能大于100'
        },
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    weight = forms.FloatField(
        label='体重（kg）',
        min_value=0,
        help_text='请输入你的体重，单位为千克',
        error_messages={
            'required': '体重是必填项',
            'min_value': '体重不能为负数'
        },
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # 身体活动水平选项
    PHYSICAL_ACTIVITY_CHOICES = [
        ('极轻', '极轻'),
        ('轻', '轻'),
        ('中', '中'),
        ('重', '重'),
        ('极重', '极重'),
    ]
    physical_activity = forms.ChoiceField(
        label='身体活动水平',
        choices=PHYSICAL_ACTIVITY_CHOICES,
        help_text='请选择你的身体活动水平',
        error_messages={
            'required': '请选择身体活动水平'
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    YesOrNo_CHOICES = [
        ('是', '是'),
        ('否', '否'),
    ]
    diabetes = forms.ChoiceField(
        label='患有糖尿病',
        choices=YesOrNo_CHOICES,
        error_messages={
            'required': '是否患有糖尿病'
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    vegetarian = forms.ChoiceField(
        label='素食主义者',
        choices=YesOrNo_CHOICES,
        error_messages={
            'required': '请选择是否为素食主义者'
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    ethnicity = forms.CharField(
        label="民族",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入民族'}
    )
    # 性别选项
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    gender = forms.ChoiceField(
        label='性别',
        choices=GENDER_CHOICES,
        help_text='请选择你的性别',
        error_messages={
            'required': '请选择你的性别'
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age<0 or age>100:
            raise forms.ValidationError("年龄需介于0-100之间")
        return age


class UserInfoForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入用户名'}
    )
    telephone = forms.CharField(
        label="手机号",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入手机号'}
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请输入密码'},
        min_length=6
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': '请再次输入密码'}
    )



    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("两次输入的密码不一致")

        return cleaned_data
