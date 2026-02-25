# API & Webhooks Module

API keys, webhooks and external integrations.

## Features

- API key generation and management with hashed storage
- Key prefix display for identification without exposing the full key
- Key expiration and last-used tracking
- Webhook configuration with target URL and event subscriptions
- Webhook secret for signature verification
- Failure count tracking for webhook deliveries
- Activate/deactivate keys and webhooks independently

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > API & Webhooks > Settings**

## Usage

Access via: **Menu > API & Webhooks**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/api_connect/dashboard/` | Overview of API keys and webhook activity |
| API Keys | `/m/api_connect/keys/` | Create and manage API keys |
| Webhooks | `/m/api_connect/webhooks/` | Configure webhook endpoints and event subscriptions |
| Settings | `/m/api_connect/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `APIKey` | API key with name, hashed key, prefix, expiration, and usage tracking |
| `Webhook` | Webhook endpoint with URL, event list, secret, and failure tracking |

## Permissions

| Permission | Description |
|------------|-------------|
| `api_connect.view_apikey` | View API keys |
| `api_connect.add_apikey` | Create new API keys |
| `api_connect.delete_apikey` | Delete API keys |
| `api_connect.view_webhook` | View webhooks |
| `api_connect.add_webhook` | Create new webhooks |
| `api_connect.change_webhook` | Edit existing webhooks |
| `api_connect.delete_webhook` | Delete webhooks |
| `api_connect.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
