"""
API & Webhooks Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('api_connect', 'dashboard')
@htmx_view('api_connect/pages/dashboard.html', 'api_connect/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('api_connect', 'keys')
@htmx_view('api_connect/pages/keys.html', 'api_connect/partials/keys_content.html')
def keys(request):
    """API Keys view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('api_connect', 'webhooks')
@htmx_view('api_connect/pages/webhooks.html', 'api_connect/partials/webhooks_content.html')
def webhooks(request):
    """Webhooks view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('api_connect', 'settings')
@htmx_view('api_connect/pages/settings.html', 'api_connect/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

