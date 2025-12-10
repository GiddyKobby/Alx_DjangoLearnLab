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