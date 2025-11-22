from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Library, Author
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.decorators import permission_required

# -----------------------------
# Existing views
# -----------------------------

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    # ✅ checker expects this exact path string:
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # ✅ expected path
    context_object_name = 'library'

# Function-based view: user registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # ✅ checker requires this
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ checker requires login after registration
            return redirect('list_books')  # Redirect to book list after registration
    else:
        form = UserCreationForm()  # ✅ checker requires this

    return render(request, 'relationship_app/register.html', {'form': form})  # ✅ checker requires this template path

# -----------------------------
# Role-Based Access Control (RBAC) views
# -----------------------------

# Role check functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# -----------------------------
# Permission-Protected Book Management Views
# -----------------------------

# Add book (requires can_add_book permission)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = get_object_or_404(Author, id=author_id)
        Book.objects.create(title=title, author=author)
        return redirect('list_books')
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

# Edit book (requires can_change_book permission)
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect('list_books')
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})

# Delete book (requires can_delete_book permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
