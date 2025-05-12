from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),

    path('user_management/', user_management, name='user_management'),
    path('clear_success_message/', clear_success_message, name='clear_success_message'),

]
