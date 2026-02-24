from django.contrib import admin

from .models import APIKey, Webhook

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'key_prefix', 'key_hash', 'is_active', 'expires_at', 'created_at']
    search_fields = ['name', 'key_prefix', 'key_hash']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active', 'secret', 'created_at']
    search_fields = ['name', 'secret']
    readonly_fields = ['created_at', 'updated_at']

