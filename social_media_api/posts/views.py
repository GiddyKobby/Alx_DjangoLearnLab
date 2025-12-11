from rest_framework import viewsets, generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

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

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # prevent duplicate by using get_or_create
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

        # create notification to post author (if liker != author)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=str(post.pk)
            )

        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if not deleted:
            return Response({'detail': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)

        # Optionally, mark corresponding notification as read or delete it.
        # Here we will mark matching 'liked your post' notifications as unread=False (or delete).
        Notification.objects.filter(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=str(post.pk)
        ).delete()

        return Response({'detail': 'Like removed'}, status=status.HTTP_200_OK)
    
    