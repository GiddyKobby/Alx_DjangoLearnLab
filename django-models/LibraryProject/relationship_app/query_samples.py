from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
author_name = "George Orwell"
books_by_author = Book.objects.filter(author__name=author_name)
print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

# Query 2: List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print(f"Books in {library_name}: {[book.title for book in books_in_library]}")

# Query 3: Retrieve the librarian for a library
librarian = Librarian.objects.get(library__name=library_name)
print(f"Librarian of {library_name}: {librarian.name}")
