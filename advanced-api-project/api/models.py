from django.db import models

class Author(models.Model):
    """
    Author model stores writer information.
    Each Author can have multiple Book entries (One-to-Many).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model stores information about individual books.
    It is linked to Author through a ForeignKey (many books per author).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'   # Enables nested serialization
    )

    def __str__(self):
        return self.title
