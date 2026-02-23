from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiConnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_connect'
    label = 'api_connect'
    verbose_name = _('API & Webhooks')

    def ready(self):
        pass
