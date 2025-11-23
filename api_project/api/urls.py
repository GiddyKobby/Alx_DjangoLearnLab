from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Token generation route
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # ListAPIView
    path('books/', BookList.as_view(), name='book-list'),

    # CRUD from ViewSet
    path('', include(router.urls)),
]
