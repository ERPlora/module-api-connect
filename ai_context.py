"""
AI context for the API Connect module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: API Connect

### Models

**APIKey** — credentials for external systems to authenticate to this Hub's API.
- `name` (str): human-readable label (e.g. "My Integration", "Mobile App")
- `key_prefix` (str, max 10): first characters of the key, shown in UI for identification
- `key_hash` (str): bcrypt/SHA hash of the actual key — the raw key is never stored
- `is_active` (bool, default True): whether this key can be used
- `expires_at` (datetime, nullable): optional expiry; null = never expires
- `last_used_at` (datetime, nullable): last time this key was used in a request

**Webhook** — outbound HTTP callbacks sent when events occur in the Hub.
- `name` (str): label for the webhook
- `url` (URL): endpoint that receives POST requests
- `events` (JSON list): list of event names to subscribe to (e.g. `["sale.created", "customer.updated"]`)
- `is_active` (bool, default True): enables/disables delivery
- `secret` (str): HMAC signing secret for verifying payload authenticity
- `last_triggered_at` (datetime, nullable): last successful delivery
- `failure_count` (int, default 0): consecutive delivery failures; high count may indicate endpoint issues

### Key flows

1. **Create API key**: generate a random key, store its hash + prefix; return the raw key once to the user.
2. **Deactivate a key**: set is_active=False.
3. **Create a webhook**: provide name, URL, event list, and optionally a secret. Set is_active=True.
4. **Disable a webhook**: set is_active=False to stop deliveries without deleting.
5. **Monitor webhooks**: check failure_count and last_triggered_at for delivery health.

### Notes
- The actual API key value is shown only once at creation — after that only key_prefix is visible.
- Events follow the pattern `"model.action"` (e.g. `"sale.created"`, `"inventory.low_stock"`).
"""
