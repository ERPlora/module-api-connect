"""
API & Webhooks Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import APIKey, Webhook

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('api_connect', 'dashboard')
@htmx_view('api_connect/pages/index.html', 'api_connect/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_api_keys': APIKey.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_webhooks': Webhook.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# APIKey
# ======================================================================

API_KEY_SORT_FIELDS = {
    'name': 'name',
    'is_active': 'is_active',
    'key_prefix': 'key_prefix',
    'key_hash': 'key_hash',
    'expires_at': 'expires_at',
    'last_used_at': 'last_used_at',
    'created_at': 'created_at',
}

def _build_api_keys_context(hub_id, per_page=10):
    qs = APIKey.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'api_keys': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_api_keys_list(request, hub_id, per_page=10):
    ctx = _build_api_keys_context(hub_id, per_page)
    return django_render(request, 'api_connect/partials/api_keys_list.html', ctx)

@login_required
@with_module_nav('api_connect', 'keys')
@htmx_view('api_connect/pages/api_keys.html', 'api_connect/partials/api_keys_content.html')
def api_keys_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = APIKey.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(key_prefix__icontains=search_query) | Q(key_hash__icontains=search_query))

    order_by = API_KEY_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_active', 'key_prefix', 'key_hash', 'expires_at', 'last_used_at']
        headers = ['Name', 'Is Active', 'Key Prefix', 'Key Hash', 'Expires At', 'Last Used At']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='api_keys.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='api_keys.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'api_connect/partials/api_keys_list.html', {
            'api_keys': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'api_keys': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def api_key_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        key_prefix = request.POST.get('key_prefix', '').strip()
        key_hash = request.POST.get('key_hash', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        expires_at = request.POST.get('expires_at') or None
        last_used_at = request.POST.get('last_used_at') or None
        obj = APIKey(hub_id=hub_id)
        obj.name = name
        obj.key_prefix = key_prefix
        obj.key_hash = key_hash
        obj.is_active = is_active
        obj.expires_at = expires_at
        obj.last_used_at = last_used_at
        obj.save()
        return _render_api_keys_list(request, hub_id)
    return django_render(request, 'api_connect/partials/panel_api_key_add.html', {})

@login_required
def api_key_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(APIKey, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.key_prefix = request.POST.get('key_prefix', '').strip()
        obj.key_hash = request.POST.get('key_hash', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.expires_at = request.POST.get('expires_at') or None
        obj.last_used_at = request.POST.get('last_used_at') or None
        obj.save()
        return _render_api_keys_list(request, hub_id)
    return django_render(request, 'api_connect/partials/panel_api_key_edit.html', {'obj': obj})

@login_required
@require_POST
def api_key_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(APIKey, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_api_keys_list(request, hub_id)

@login_required
@require_POST
def api_key_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(APIKey, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_api_keys_list(request, hub_id)

@login_required
@require_POST
def api_keys_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = APIKey.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_api_keys_list(request, hub_id)


# ======================================================================
# Webhook
# ======================================================================

WEBHOOK_SORT_FIELDS = {
    'name': 'name',
    'is_active': 'is_active',
    'failure_count': 'failure_count',
    'url': 'url',
    'secret': 'secret',
    'created_at': 'created_at',
}

def _build_webhooks_context(hub_id, per_page=10):
    qs = Webhook.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'webhooks': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_webhooks_list(request, hub_id, per_page=10):
    ctx = _build_webhooks_context(hub_id, per_page)
    return django_render(request, 'api_connect/partials/webhooks_list.html', ctx)

@login_required
@with_module_nav('api_connect', 'webhooks')
@htmx_view('api_connect/pages/webhooks.html', 'api_connect/partials/webhooks_content.html')
def webhooks_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Webhook.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(secret__icontains=search_query))

    order_by = WEBHOOK_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_active', 'failure_count', 'url', 'events', 'secret']
        headers = ['Name', 'Is Active', 'Failure Count', 'Url', 'Events', 'Secret']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='webhooks.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='webhooks.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'api_connect/partials/webhooks_list.html', {
            'webhooks': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'webhooks': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def webhook_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        url = request.POST.get('url', '').strip()
        events = request.POST.get('events', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        secret = request.POST.get('secret', '').strip()
        last_triggered_at = request.POST.get('last_triggered_at') or None
        failure_count = int(request.POST.get('failure_count', 0) or 0)
        obj = Webhook(hub_id=hub_id)
        obj.name = name
        obj.url = url
        obj.events = events
        obj.is_active = is_active
        obj.secret = secret
        obj.last_triggered_at = last_triggered_at
        obj.failure_count = failure_count
        obj.save()
        return _render_webhooks_list(request, hub_id)
    return django_render(request, 'api_connect/partials/panel_webhook_add.html', {})

@login_required
def webhook_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Webhook, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.url = request.POST.get('url', '').strip()
        obj.events = request.POST.get('events', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.secret = request.POST.get('secret', '').strip()
        obj.last_triggered_at = request.POST.get('last_triggered_at') or None
        obj.failure_count = int(request.POST.get('failure_count', 0) or 0)
        obj.save()
        return _render_webhooks_list(request, hub_id)
    return django_render(request, 'api_connect/partials/panel_webhook_edit.html', {'obj': obj})

@login_required
@require_POST
def webhook_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Webhook, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_webhooks_list(request, hub_id)

@login_required
@require_POST
def webhook_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Webhook, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_webhooks_list(request, hub_id)

@login_required
@require_POST
def webhooks_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Webhook.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_webhooks_list(request, hub_id)


@login_required
@with_module_nav('api_connect', 'settings')
@htmx_view('api_connect/pages/settings.html', 'api_connect/partials/settings_content.html')
def settings_view(request):
    return {}

