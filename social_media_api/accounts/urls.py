from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowUserView, UnfollowUserView, FollowingListView, FollowersListView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),   # existing
    path('login/', LoginView.as_view(), name='login'),            # existing
    path('profile/', ProfileView.as_view(), name='profile'),      # existing

    # follow / unfollow
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),

    # listing a user's following/followers
    path('<int:user_id>/following/', FollowingListView.as_view(), name='user-following'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='user-followers'),
]
