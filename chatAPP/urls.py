from django.urls import path

from chatAPP import views

urlpatterns = [
    # 其他 URL 配置
    path('get_answer/', views.get_answer, name='get_answer'),
   
    # path('index/', views.index, name='index'),
    # path('conversation/<int:conversation_id>/', views.get_conversation, name='get_conversation'),
    # path('add_message/', views.add_message, name='add_message'),
    # path('new_conversation/', views.new_conversation, name='new_conversation'),
    # path('clear_conversation/<int:conversation_id>/', views.clear_conversation, name='clear_conversation'),
]
