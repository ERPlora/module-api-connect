from django.urls import path
from . import views

app_name = 'api_connect'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('keys/', views.api_keys_list, name='keys'),


    # APIKey
    path('api_keys/', views.api_keys_list, name='api_keys_list'),
    path('api_keys/add/', views.api_key_add, name='api_key_add'),
    path('api_keys/<uuid:pk>/edit/', views.api_key_edit, name='api_key_edit'),
    path('api_keys/<uuid:pk>/delete/', views.api_key_delete, name='api_key_delete'),
    path('api_keys/<uuid:pk>/toggle/', views.api_key_toggle_status, name='api_key_toggle_status'),
    path('api_keys/bulk/', views.api_keys_bulk_action, name='api_keys_bulk_action'),

    # Webhook
    path('webhooks/', views.webhooks_list, name='webhooks_list'),
    path('webhooks/add/', views.webhook_add, name='webhook_add'),
    path('webhooks/<uuid:pk>/edit/', views.webhook_edit, name='webhook_edit'),
    path('webhooks/<uuid:pk>/delete/', views.webhook_delete, name='webhook_delete'),
    path('webhooks/<uuid:pk>/toggle/', views.webhook_toggle_status, name='webhook_toggle_status'),
    path('webhooks/bulk/', views.webhooks_bulk_action, name='webhooks_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
