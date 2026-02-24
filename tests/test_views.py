"""Tests for api_connect views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('api_connect:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('api_connect:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('api_connect:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestAPIKeyViews:
    """APIKey view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('api_connect:api_keys_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('api_connect:api_keys_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('api_connect:api_keys_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('api_connect:api_keys_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('api_connect:api_keys_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('api_connect:api_keys_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('api_connect:api_key_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('api_connect:api_key_add')
        data = {
            'name': 'New Name',
            'key_prefix': 'New Key Prefix',
            'key_hash': 'New Key Hash',
            'is_active': 'on',
            'expires_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, api_key):
        """Test edit form loads."""
        url = reverse('api_connect:api_key_edit', args=[api_key.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, api_key):
        """Test editing via POST."""
        url = reverse('api_connect:api_key_edit', args=[api_key.pk])
        data = {
            'name': 'Updated Name',
            'key_prefix': 'Updated Key Prefix',
            'key_hash': 'Updated Key Hash',
            'is_active': '',
            'expires_at': '2025-01-15T10:00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, api_key):
        """Test soft delete via POST."""
        url = reverse('api_connect:api_key_delete', args=[api_key.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        api_key.refresh_from_db()
        assert api_key.is_deleted is True

    def test_toggle_status(self, auth_client, api_key):
        """Test toggle active status."""
        url = reverse('api_connect:api_key_toggle_status', args=[api_key.pk])
        original = api_key.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        api_key.refresh_from_db()
        assert api_key.is_active != original

    def test_bulk_delete(self, auth_client, api_key):
        """Test bulk delete."""
        url = reverse('api_connect:api_keys_bulk_action')
        response = auth_client.post(url, {'ids': str(api_key.pk), 'action': 'delete'})
        assert response.status_code == 200
        api_key.refresh_from_db()
        assert api_key.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('api_connect:api_keys_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestWebhookViews:
    """Webhook view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('api_connect:webhooks_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('api_connect:webhooks_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('api_connect:webhooks_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('api_connect:webhooks_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('api_connect:webhooks_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('api_connect:webhooks_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('api_connect:webhook_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('api_connect:webhook_add')
        data = {
            'name': 'New Name',
            'url': 'https://example.com',
            'events': 'test',
            'is_active': 'on',
            'secret': 'New Secret',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, webhook):
        """Test edit form loads."""
        url = reverse('api_connect:webhook_edit', args=[webhook.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, webhook):
        """Test editing via POST."""
        url = reverse('api_connect:webhook_edit', args=[webhook.pk])
        data = {
            'name': 'Updated Name',
            'url': 'https://example.com',
            'events': 'test',
            'is_active': '',
            'secret': 'Updated Secret',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, webhook):
        """Test soft delete via POST."""
        url = reverse('api_connect:webhook_delete', args=[webhook.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        webhook.refresh_from_db()
        assert webhook.is_deleted is True

    def test_toggle_status(self, auth_client, webhook):
        """Test toggle active status."""
        url = reverse('api_connect:webhook_toggle_status', args=[webhook.pk])
        original = webhook.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        webhook.refresh_from_db()
        assert webhook.is_active != original

    def test_bulk_delete(self, auth_client, webhook):
        """Test bulk delete."""
        url = reverse('api_connect:webhooks_bulk_action')
        response = auth_client.post(url, {'ids': str(webhook.pk), 'action': 'delete'})
        assert response.status_code == 200
        webhook.refresh_from_db()
        assert webhook.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('api_connect:webhooks_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('api_connect:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('api_connect:settings')
        response = client.get(url)
        assert response.status_code == 302

