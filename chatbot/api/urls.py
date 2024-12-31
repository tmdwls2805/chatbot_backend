# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('read-txt-files', views.read_txt_files, name='read_txt_files'),
    path('gpt-3-turbo', views.gpt_3_turbo, name='gpt_3_turbo'),
    path('gpt-4', views.gpt_4, name='gpt_4'),
    path('gpt-4-turbo', views.gpt_4_turbo, name='gpt_4_turbo'),
    path('gpt-4o', views.gpt_4o, name='gpt_4o'),
    path('gpt-4o-mini', views.gpt_4o_mini, name='gpt_4o_mini'),
    path('home/', views.HomeView.as_view(), name='home'),
]
