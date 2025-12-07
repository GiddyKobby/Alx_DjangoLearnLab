from django.urls import path
from . import views

from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='home'),
    path('posts/', views.posts, name='posts'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    

    path('', views.post_list, name='post_list'),

    # Create
    path('post/new/', views.post_create, name='post_create'),

    # Read single post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # Update
    path('post/<int:pk>/update/', views.post_update, name='post_update'),

    # Delete
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

     # Comments
    path('post/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]