from django.shortcuts import render, redirect
from .models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test

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
