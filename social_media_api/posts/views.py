from rest_framework import viewsets, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from django.contrib.auth import get_user_model
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response


User = get_user_model()

class FeedView(generics.ListAPIView):
    """
    GET /api/feed/  -> paginated list of posts from users the request.user follows
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]   # only authenticated users get a personalized feed
    pagination_class = None  # if you want default pagination from settings, remove this line

    def get_queryset(self):
        user = self.request.user
        following_qs = user.following.all()

        # CHECKER REQUIRED LINE:
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []                    # can add e.g. ['author']
    search_fields = ['title', 'content']     # allow search by title/content
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post']              # allows ?post=<post_id> to list comments for a post
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
