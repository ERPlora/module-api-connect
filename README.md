# API & Webhooks

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `api_connect` |
| **Version** | `1.0.0` |
| **Icon** | `code-slash-outline` |
| **Dependencies** | None |

## Models

### `APIKey`

APIKey(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, key_prefix, key_hash, is_active, expires_at, last_used_at)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `key_prefix` | CharField | max_length=10 |
| `key_hash` | CharField | max_length=255 |
| `is_active` | BooleanField |  |
| `expires_at` | DateTimeField | optional |
| `last_used_at` | DateTimeField | optional |

### `Webhook`

Webhook(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, url, events, is_active, secret, last_triggered_at, failure_count)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `url` | URLField | max_length=200 |
| `events` | JSONField |  |
| `is_active` | BooleanField |  |
| `secret` | CharField | max_length=255, optional |
| `last_triggered_at` | DateTimeField | optional |
| `failure_count` | PositiveIntegerField |  |

## URL Endpoints

Base path: `/m/api_connect/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `keys/` | `keys` | GET |
| `api_keys/` | `api_keys_list` | GET |
| `api_keys/add/` | `api_key_add` | GET/POST |
| `api_keys/<uuid:pk>/edit/` | `api_key_edit` | GET |
| `api_keys/<uuid:pk>/delete/` | `api_key_delete` | GET/POST |
| `api_keys/<uuid:pk>/toggle/` | `api_key_toggle_status` | GET |
| `api_keys/bulk/` | `api_keys_bulk_action` | GET/POST |
| `webhooks/` | `webhooks_list` | GET |
| `webhooks/add/` | `webhook_add` | GET/POST |
| `webhooks/<uuid:pk>/edit/` | `webhook_edit` | GET |
| `webhooks/<uuid:pk>/delete/` | `webhook_delete` | GET/POST |
| `webhooks/<uuid:pk>/toggle/` | `webhook_toggle_status` | GET |
| `webhooks/bulk/` | `webhooks_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `api_connect.view_apikey` | View Apikey |
| `api_connect.add_apikey` | Add Apikey |
| `api_connect.delete_apikey` | Delete Apikey |
| `api_connect.view_webhook` | View Webhook |
| `api_connect.add_webhook` | Add Webhook |
| `api_connect.change_webhook` | Change Webhook |
| `api_connect.delete_webhook` | Delete Webhook |
| `api_connect.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_apikey`, `add_webhook`, `change_webhook`, `view_apikey`, `view_webhook`
- **employee**: `add_apikey`, `view_apikey`, `view_webhook`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| API Keys | `key-outline` | `keys` | No |
| Webhooks | `code-slash-outline` | `webhooks` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_api_keys`

List API keys.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |

### `list_webhooks`

List configured webhooks.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |

### `create_webhook`

Create a webhook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes |  |
| `url` | string | Yes |  |
| `events` | array | Yes |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  api_connect/
    css/
    js/
  icons/
    icon.svg
templates/
  api_connect/
    pages/
      api_key_add.html
      api_key_edit.html
      api_keys.html
      dashboard.html
      index.html
      keys.html
      settings.html
      webhook_add.html
      webhook_edit.html
      webhooks.html
    partials/
      api_key_add_content.html
      api_key_edit_content.html
      api_keys_content.html
      api_keys_list.html
      dashboard_content.html
      keys_content.html
      panel_api_key_add.html
      panel_api_key_edit.html
      panel_webhook_add.html
      panel_webhook_edit.html
      settings_content.html
      webhook_add_content.html
      webhook_edit_content.html
      webhooks_content.html
      webhooks_list.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
