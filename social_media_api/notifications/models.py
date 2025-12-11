from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='actor_notifications')
    verb = models.CharField(max_length=255)            # e.g. "liked", "commented", "followed"
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Generic target
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)  # keep char for versatility
    target = GenericForeignKey('target_content_type', 'target_object_id')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification to {self.recipient}: {self.actor} {self.verb}"
