from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'unread', 'timestamp', 'target_repr']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'timestamp', 'target_repr']

    def get_target_repr(self, obj):
        # safe textual representation of target
        try:
            return str(obj.target)
        except Exception:
            return None
