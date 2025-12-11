# accounts/tests.py
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from posts.models import Post

User = get_user_model()

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass1234')
        self.bob = User.objects.create_user(username='bob', password='pass1234')
        self.carol = User.objects.create_user(username='carol', password='pass1234')
        # Bob and Carol create posts
        Post.objects.create(author=self.bob, title='B1', content='bob post')
        Post.objects.create(author=self.carol, title='C1', content='carol post')

    def test_follow_and_feed(self):
        # alice logs in
        self.client.force_authenticate(user=self.alice)
        follow_url = f'/api/accounts/follow/{self.bob.id}/'
        resp = self.client.post(follow_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # alice's feed should include bob's post
        feed_resp = self.client.get('/api/feed/')
        self.assertEqual(feed_resp.status_code, status.HTTP_200_OK)
        results = feed_resp.data.get('results') if 'results' in feed_resp.data else feed_resp.data
        self.assertTrue(any(p['title'] == 'B1' for p in results))
        # ensure carol's post not included until alice follows carol
        self.assertFalse(any(p['title'] == 'C1' for p in results))
        # follow carol and recheck
        self.client.post(f'/api/accounts/follow/{self.carol.id}/')
        feed_resp2 = self.client.get('/api/feed/')
        results2 = feed_resp2.data.get('results') if 'results' in feed_resp2.data else feed_resp2.data
        titles = [p['title'] for p in results2]
        self.assertIn('C1', titles)
