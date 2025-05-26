from django.shortcuts import redirect
from functools import wraps

def check_login(view_func):
    """自定义登录验证装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 验证session中的uid存在性
        print("进入装饰器验证")
        print("当前Session ID:", request.session.session_key)
        print("Session内容:", request.session.get('uid'))

        if not request.session.get('user_id'):
            # 记录来源地址用于跳转
            return redirect(f'/User/login/')
        return view_func(request, *args, **kwargs)
    return wrapper