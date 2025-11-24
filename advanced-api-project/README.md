## API Endpoints

### Books
- GET /api/books/ — List all books
- GET /api/books/<id>/ — Retrieve one book
- POST /api/books/create/ — Create a book (Auth required)
- PATCH /api/books/<id>/update/ — Update book (Auth required)
- DELETE /api/books/<id>/delete/ — Delete book (Auth required)

## Permissions
- List & Detail: Public
- Create, Update, Delete: Authenticated users only
