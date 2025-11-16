
### **update.md**
```markdown
# Update a Book instance

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
# Expected output:
# <Book: Nineteen Eighty-Four by George Orwell (1949)>
