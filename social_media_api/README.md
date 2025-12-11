Setup

Clone repo Alx_DjangoLearnLab and cd social_media_api.

Create and activate virtualenv.

pip install -r requirements.txt

python manage.py makemigrations && python manage.py migrate

python manage.py runserver

Endpoints

POST /api/accounts/register/ — register and get token.

POST /api/accounts/login/ — login and get token.

GET|PUT /api/accounts/profile/ — get or update your profile (auth required).

Notes

profile_picture uses Django media settings; install Pillow.

The followers field is ManyToMany to the same User model (asymmetric). Use user.followers.add(other_user) to add.



# Posts API
GET /api/posts/            List posts (paginated)
POST /api/posts/           Create post (auth required)
GET /api/posts/{id}/       Retrieve post with comments
PUT/PATCH /api/posts/{id}/ Update (author only)
DELETE /api/posts/{id}/    Delete (author only)

# Comments API
GET /api/comments/         List comments (filter by ?post=<id>)
POST /api/comments/        Create comment (auth required)
GET /api/comments/{id}/    Retrieve comment
PUT/PATCH /api/comments/{id}/ Update (author only)
DELETE /api/comments/{id}/ Delete (author only)

Search posts: GET /api/posts/?search=keyword
Pagination: ?page=2
