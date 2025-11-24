from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class BookListView(generics.ListAPIView):
    """
    GET: Return a list of all books with support for:
    - Filtering
    - Searching
    - Ordering
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Add filtering, searching, ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Filtering fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Search fields (partial match)
    search_fields = ['title', 'author__name']

    # Ordering fields
    ordering_fields = ['title', 'publication_year']

    # Default ordering
    ordering = ['title']

    """
Filtering available:
    /api/books/?title=SomeTitle
    /api/books/?author=1
    /api/books/?publication_year=2024

Searching available:
    /api/books/?search=python

Ordering available:
    /api/books/?ordering=title
    /api/books/?ordering=-publication_year
"""


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Return a single book by ID.
    Accessible to everyone (Read Only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom behavior for creation.
        Ensures data is fully validated before saving.
        """
        serializer.is_valid(raise_exception=True)
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update logic.
        Ensures full validation.
        """
        serializer.is_valid(raise_exception=True)
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
