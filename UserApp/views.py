import hashlib
import re

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .auth import check_login
from .forms import LoginForm, RegisterForm, UserBasicInfoForm, UserInfoForm
from django.contrib import messages
from UserApp.models import *
import logging
@check_login
def index(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # 对密码进行加密（与注册时相同的加密方式）
            encrypted_password = hashlib.sha256(password.encode()).hexdigest()
            try:
                user = UserInfo.objects.get(username=username,password=encrypted_password)
                request.session['user_id'] = user.uid
                request.session.set_expiry(3600)  # 设置1小时过期（可选）
                request.session.save()
                return render(request, 'home.html')  # 登录成功后重定向到首页
            except UserInfo.DoesNotExist:
                messages.error(request, "用户名或密码错误")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


import hashlib
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserInfo
from .forms import RegisterForm

def validate_telephone(value):
    pattern = r'^1[3-9]\d{9}$'  # 中国手机号格式：1开头，第二位3-9，共11位
    if not re.match(pattern, value):
        return '手机号格式不正确'
    else:
        return True
def user_register(request):
    success_message = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 获取表单中的用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            telephone = form.cleaned_data['telephone']


            # 对密码进行加密
            encrypted_password = hashlib.sha256(password.encode()).hexdigest()

            user = UserInfo.objects.filter(username=username).first()
            if user:
                success_message ="注册失败，当前系统已存在该名称用户"
            else:
                # 验证手机号格式
                result = validate_telephone(telephone)
                if result is not True:
                    messages.error(request,result)
                try:
                    # 创建新用户
                    UserInfo.objects.create(
                        username=username,
                        password=encrypted_password,
                        telephone=telephone,
                    )
                    user = UserInfo.objects.filter(username=username,password=encrypted_password).first()
                    UserBasicInfo.objects.create(
                        uid=user,
                        gender='F',
                        weight=0,
                        height=0,
                        age=0,
                        physical_activity=1,
                        diabetes='N',
                        ethnicity='汉族',
                        vegetarian='N'
                    )
                    # 注册成功提示
                    success_message = "注册成功，请登录"
                    # 将成功消息存储在会话中，以便重定向后仍能访问
                    request.session['success_message'] = success_message
                except Exception as e:
                    # 处理创建用户时可能出现的异常，例如用户名重复等
                    print(str(e))
                    messages.error(request, f"注册失败: {str(e)}")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form,'success_message': success_message})


def user_logout(request):
    request.session.flush()
    # messages.success(request, '退出成功！')
    return redirect('login')


@check_login
def user_management(request):
    success_message = None
    form_error = None

    user_basic_info_form = UserBasicInfoForm()
    user_info_form = UserInfoForm()

    uid = request.session.get("user_id")
    user_info = UserInfo.objects.filter(uid=uid).first()
    user_basic_info = UserBasicInfo.objects.filter(uid=uid).first()
    print(user_basic_info.physical_activity)

    active_tab = "Tab1"

    if request.method == 'POST':
        tab = request.POST.get("Tab_value")
        if tab == '2':
            active_tab = "Tab2"
            form = UserBasicInfoForm(request.POST)
            if form.is_valid():
                # 处理表单数据
                height = form.cleaned_data['height']
                age = form.cleaned_data['age']
                weight = form.cleaned_data['weight']
                physical_activity = form.cleaned_data['physical_activity']
                gender = form.cleaned_data['gender']
                diabetes = form.cleaned_data['diabetes']
                ethnicity = form.cleaned_data['ethnicity']
                vegetarian=form.cleaned_data['vegetarian']
                uid = request.session.get("user_id")
                # INSERT_YOUR_CODE
                # 检查user_basic_info是否存在且关键字段有变化
                need_update_meal_recommend = False
                if user_basic_info:
                    if (
                        user_basic_info.age != age or
                        user_basic_info.vegetarian != vegetarian or
                        user_basic_info.weight != weight or
                        user_basic_info.physical_activity != physical_activity
                    ):
                        need_update_meal_recommend = True
                else:
                    # 如果没有user_basic_info，说明是新建，也需要更新
                    need_update_meal_recommend = True

                if need_update_meal_recommend:
                    from UserApp.models import MealRecommend
                    # 删除该用户的meal_recommend表内容
                    MealRecommend.objects.filter(uid=uid).delete()
                    # 获取当前登录用户名
                    username = None
                    if user_info:
                        username = user_info.username
                    if username:
                        import threading
                        from mcp_tools.save_meal_recommend import save_meal_recommend

                        def run_save_meal_recommend(username):
                            try:
                                save_meal_recommend(username)
                            except Exception as e:
                                print(f"save_meal_recommend error: {e}")

                        threading.Thread(target=run_save_meal_recommend, args=(username,), daemon=True).start()
                try:
                    user_basic_info = UserBasicInfo()
                    user_basic_info.uid = UserInfo.objects.get(uid=uid)
                    user_basic_info.height = height
                    user_basic_info.age = age
                    user_basic_info.weight = weight
                    user_basic_info.physical_activity = physical_activity
                    user_basic_info.gender= gender
                    user_basic_info.diabetes = diabetes
                    user_basic_info.ethnicity = ethnicity
                    user_basic_info.vegetarian = vegetarian
                    user_basic_info.save()
                    success_message = "保存成功！"
                    user_basic_info = UserBasicInfo.objects.filter(uid=uid).first()
                    user_basic_info_form = UserBasicInfoForm(initial={
                        'height':user_basic_info.height,
                        'age':user_basic_info.age,
                        'weight':user_basic_info.weight,
                        'physical_activity':user_basic_info.physical_activity,
                        'gender':user_basic_info.gender,
                        'diabetes':user_basic_info.diabetes,
                        'ethnicity':user_basic_info.ethnicity,
                        'vegetarian':user_basic_info.vegetarian
                    })
                except UserBasicInfo.DoesNotExist:
                    form_error = "用户健康信息不存在"
            else:
                form_error = form.errors
        elif tab == '1':
            form = UserInfoForm(request.POST)
            if form.is_valid():
                # 处理表单数据
                username = form.cleaned_data['username']
                telephone = form.cleaned_data['telephone']
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']


                if password == confirm_password and validate_telephone(telephone) is True:
                    uid = request.session.get("user_id")
                    try:
                        user = UserInfo.objects.get(uid=uid)
                        user.username=username
                        user.password = hashlib.sha256(password.encode()).hexdigest()
                        user.telephone = telephone
                        user.save()
                        user_info = UserInfo.objects.filter(uid=uid).first()
                        success_message = "保存成功！"
                        user_info_form = UserInfoForm()
                    except UserInfo.DoesNotExist:
                        form_error = "用户不存在"
                else:
                    form_error = "修改失败，请检查手机号或密码"
            else:
                form_error = form.errors
        return render(request, 'user_management.html',
                      {'user_basic_info_form': user_basic_info_form, 'user_info_form': user_info_form,
                       'success_message': success_message, 'form_error': form_error, 'active_tab':active_tab,'user_info': user_info,'user_basic_info':user_basic_info})
    else:
        user_basic_info = UserBasicInfo.objects.filter(uid=uid).first()
        user_basic_info_form = UserBasicInfoForm(initial={
            'height': user_basic_info.height,
            'age': user_basic_info.age,
            'weight': user_basic_info.weight,
            'physical_activity': user_basic_info.physical_activity,
            'gender': user_basic_info.gender,
            'diabetes': user_basic_info.diabetes,
            'ethnicity': user_basic_info.ethnicity,
            'vegetarian': user_basic_info.vegetarian
        })
        return render(request, 'user_management.html',
                      {'user_basic_info_form': user_basic_info_form, 'user_info_form': user_info_form,
                       'success_message': success_message, 'form_error': form_error, 'user_info': user_info,'user_basic_info':user_basic_info})





def clear_success_message(request):
    if'success_message' in request.session:
        del request.session['success_message']
    return JsonResponse({'status': 'success'})