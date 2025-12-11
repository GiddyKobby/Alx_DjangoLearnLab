from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Post, Like
from notifications.models import Notification

User = get_user_model()

class PostCommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass1234')
        self.user2 = User.objects.create_user(username='bob', password='pass1234')
        self.post = Post.objects.create(author=self.user, title='T', content='C')

    def test_create_post_requires_auth(self):
        url = reverse('post-list')  # router name
        data = {'title': 'New', 'content': 'Body'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # authenticate
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(url, data, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)

    def test_only_author_can_delete(self):
        url = reverse('post-detail', args=[self.post.id])
        # bob tries delete
        self.client.force_authenticate(user=self.user2)
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED))
        # owner deletes
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.delete(url)
        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)

class LikeTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass1234')
        self.bob = User.objects.create_user(username='bob', password='pass1234')
        self.post = Post.objects.create(author=self.bob, title='B1', content='bob post')

    def test_like_creates_notification(self):
        self.client.force_authenticate(user=self.alice)
        resp = self.client.post(f'/api/posts/{self.post.pk}/like/')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.alice).exists())
        # notification created for bob
        self.assertTrue(Notification.objects.filter(recipient=self.bob, actor=self.alice, verb__icontains='liked').exists())

    def test_unlike_removes_like_and_notification(self):
        self.client.force_authenticate(user=self.alice)
        self.client.post(f'/api/posts/{self.post.pk}/like/')
        resp = self.client.post(f'/api/posts/{self.post.pk}/unlike/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(post=self.post, user=self.alice).exists())
        self.assertFalse(Notification.objects.filter(recipient=self.bob, actor=self.alice, verb__icontains='liked').exists())

