from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from posts.models import Post
from notifications.models import Notification

User = get_user_model()

class NotificationsTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass1234')
        self.bob = User.objects.create_user(username='bob', password='pass1234')
        self.post = Post.objects.create(author=self.bob, title='B', content='c')
        Notification.objects.create(recipient=self.bob, actor=self.alice, verb='liked your post')

    def test_list_notifications(self):
        self.client.force_authenticate(user=self.bob)
        resp = self.client.get('/api/notifications/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data.get('results', resp.data)), 1)

    def test_mark_all_read(self):
        self.client.force_authenticate(user=self.bob)
        resp = self.client.post('/api/notifications/mark-all-read/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(Notification.objects.filter(recipient=self.bob, unread=True).exists())
