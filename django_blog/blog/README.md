# Blog Post Management (CRUD)

This module allows users to create, read, update, and delete blog posts.

## Features
- List all posts
- View a single post
- Create post (login required)
- Edit post (author only)
- Delete post (author only)

## Permissions
- Public can browse posts.
- Authenticated users can publish posts.
- Only the author can modify or delete posts.

# Comment System

This blog supports user comments with full CRUD functionality.

## Features
- View all comments under each post
- Authenticated users can submit comments
- Comment authors can edit or delete their own comments
- Comments show newest first
- Integrated directly into post detail page

## Permissions
- Anyone may read comments
- Only logged-in users may comment
- Only comment authors may edit/delete their own comments


## Tagging & Search

### Tags
- Add tags to posts using the `tag_string` field when creating or editing a post (comma-separated).
- Tags are stored in the `Tag` model and linked to posts via a ManyToMany relation.
- Click a tag to view all posts with that tag. URL format: `/tags/<tag_name>/`.

### Search
- Use the search bar (GET `q`) to find posts by title, content, or tag name.
- Search results page: `/search/?q=your+terms`.

### Developer notes
- After changing models, run migrations:
