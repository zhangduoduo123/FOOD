from django.urls import path

from chatAPP import views

urlpatterns = [
    # 其他 URL 配置
    path('get_answer/', views.get_answer, name='get_answer'),
]