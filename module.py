    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'api_connect'
    MODULE_NAME = _('API & Webhooks')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'code-slash-outline'
    MODULE_DESCRIPTION = _('API keys, webhooks and external integrations')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'integrations'

    MENU = {
        'label': _('API & Webhooks'),
        'icon': 'code-slash-outline',
        'order': 85,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('API Keys'), 'icon': 'key-outline', 'id': 'keys'},
{'label': _('Webhooks'), 'icon': 'code-slash-outline', 'id': 'webhooks'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'api_connect.view_apikey',
'api_connect.add_apikey',
'api_connect.delete_apikey',
'api_connect.view_webhook',
'api_connect.add_webhook',
'api_connect.change_webhook',
'api_connect.delete_webhook',
'api_connect.manage_settings',
    ]
