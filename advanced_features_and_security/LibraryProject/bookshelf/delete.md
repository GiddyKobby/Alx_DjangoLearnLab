
### **delete.md**
```markdown
# Delete a Book instance

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# Expected output:
# <QuerySet []>
