from rest_framework import generics, permissions, status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notif.unread = False
        notif.save()
        return Response({'detail': 'Marked read'}, status=status.HTTP_200_OK)

class MarkAllReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
        return Response({'detail': 'All notifications marked read'}, status=status.HTTP_200_OK)
