from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class APIKey(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    key_prefix = models.CharField(max_length=10, verbose_name=_('Key Prefix'))
    key_hash = models.CharField(max_length=255, verbose_name=_('Key Hash'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Expires At'))
    last_used_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Used At'))

    class Meta(HubBaseModel.Meta):
        db_table = 'api_connect_apikey'

    def __str__(self):
        return self.name


class Webhook(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    url = models.URLField(verbose_name=_('Url'))
    events = models.JSONField(default=list, verbose_name=_('Events'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    secret = models.CharField(max_length=255, blank=True, verbose_name=_('Secret'))
    last_triggered_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Triggered At'))
    failure_count = models.PositiveIntegerField(default=0, verbose_name=_('Failure Count'))

    class Meta(HubBaseModel.Meta):
        db_table = 'api_connect_webhook'

    def __str__(self):
        return self.name

