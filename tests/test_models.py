"""Tests for api_connect models."""
import pytest
from django.utils import timezone

from api_connect.models import APIKey, Webhook


@pytest.mark.django_db
class TestAPIKey:
    """APIKey model tests."""

    def test_create(self, api_key):
        """Test APIKey creation."""
        assert api_key.pk is not None
        assert api_key.is_deleted is False

    def test_str(self, api_key):
        """Test string representation."""
        assert str(api_key) is not None
        assert len(str(api_key)) > 0

    def test_soft_delete(self, api_key):
        """Test soft delete."""
        pk = api_key.pk
        api_key.is_deleted = True
        api_key.deleted_at = timezone.now()
        api_key.save()
        assert not APIKey.objects.filter(pk=pk).exists()
        assert APIKey.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, api_key):
        """Test default queryset excludes deleted."""
        api_key.is_deleted = True
        api_key.deleted_at = timezone.now()
        api_key.save()
        assert APIKey.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, api_key):
        """Test toggling is_active."""
        original = api_key.is_active
        api_key.is_active = not original
        api_key.save()
        api_key.refresh_from_db()
        assert api_key.is_active != original


@pytest.mark.django_db
class TestWebhook:
    """Webhook model tests."""

    def test_create(self, webhook):
        """Test Webhook creation."""
        assert webhook.pk is not None
        assert webhook.is_deleted is False

    def test_str(self, webhook):
        """Test string representation."""
        assert str(webhook) is not None
        assert len(str(webhook)) > 0

    def test_soft_delete(self, webhook):
        """Test soft delete."""
        pk = webhook.pk
        webhook.is_deleted = True
        webhook.deleted_at = timezone.now()
        webhook.save()
        assert not Webhook.objects.filter(pk=pk).exists()
        assert Webhook.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, webhook):
        """Test default queryset excludes deleted."""
        webhook.is_deleted = True
        webhook.deleted_at = timezone.now()
        webhook.save()
        assert Webhook.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, webhook):
        """Test toggling is_active."""
        original = webhook.is_active
        webhook.is_active = not original
        webhook.save()
        webhook.refresh_from_db()
        assert webhook.is_active != original


