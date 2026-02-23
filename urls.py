from django.urls import path
from . import views

app_name = 'api_connect'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('keys/', views.keys, name='keys'),
    path('webhooks/', views.webhooks, name='webhooks'),
    path('settings/', views.settings, name='settings'),
]
