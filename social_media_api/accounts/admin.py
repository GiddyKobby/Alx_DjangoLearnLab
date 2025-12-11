from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    fieldsets = (*BaseUserAdmin.fieldsets,)
    list_display = ('username', 'email', 'is_staff')
