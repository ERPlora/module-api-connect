from django import forms
from django.utils.translation import gettext_lazy as _

from .models import APIKey, Webhook

class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKey
        fields = ['name', 'key_prefix', 'key_hash', 'is_active', 'expires_at', 'last_used_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'key_prefix': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'key_hash': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'expires_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'last_used_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
        }

class WebhookForm(forms.ModelForm):
    class Meta:
        model = Webhook
        fields = ['name', 'url', 'events', 'is_active', 'secret', 'last_triggered_at', 'failure_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'url': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'url'}),
            'events': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'secret': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'last_triggered_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'failure_count': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

