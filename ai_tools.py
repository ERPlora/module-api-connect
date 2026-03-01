"""AI tools for the API Connect module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListAPIKeys(AssistantTool):
    name = "list_api_keys"
    description = "List API keys."
    module_id = "api_connect"
    required_permission = "api_connect.view_apikey"
    parameters = {"type": "object", "properties": {"is_active": {"type": "boolean"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from api_connect.models import APIKey
        qs = APIKey.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        return {"keys": [{"id": str(k.id), "name": k.name, "key_prefix": k.key_prefix, "is_active": k.is_active, "expires_at": k.expires_at.isoformat() if k.expires_at else None, "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None} for k in qs]}


@register_tool
class ListWebhooks(AssistantTool):
    name = "list_webhooks"
    description = "List configured webhooks."
    module_id = "api_connect"
    required_permission = "api_connect.view_webhook"
    parameters = {"type": "object", "properties": {"is_active": {"type": "boolean"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from api_connect.models import Webhook
        qs = Webhook.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        return {"webhooks": [{"id": str(w.id), "name": w.name, "url": w.url, "events": w.events, "is_active": w.is_active, "failure_count": w.failure_count} for w in qs]}


@register_tool
class CreateWebhook(AssistantTool):
    name = "create_webhook"
    description = "Create a webhook."
    module_id = "api_connect"
    required_permission = "api_connect.add_webhook"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "url": {"type": "string"}, "events": {"type": "array", "items": {"type": "string"}}},
        "required": ["name", "url", "events"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from api_connect.models import Webhook
        w = Webhook.objects.create(name=args['name'], url=args['url'], events=args['events'])
        return {"id": str(w.id), "name": w.name, "created": True}
