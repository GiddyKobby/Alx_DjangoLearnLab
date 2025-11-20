# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
    """
    Extend UserManager so create_user/create_superuser accept our extra fields.
    We call super() to leverage built-in behaviour and include extra fields.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        # optional: enforce date_of_birth present if you want
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email=email, password=password, **extra_fields)


def user_profile_photo_path(instance, filename):
    # e.g. media/profile_photos/user_<id>/<filename>
    return f'profile_photos/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    """
    Custom user extending Django's AbstractUser, adding date_of_birth and profile_photo.
    Keep username/email behavior from AbstractUser; change as needed.
    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to=user_profile_photo_path, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

