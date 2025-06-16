from django.urls import path

from knowledgeApp import views

urlpatterns = [
       path('knowledge/', views.knowledge, name='knowledge'),
]
