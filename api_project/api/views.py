from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView

# Original list-only view
class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ViewSet for full CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
