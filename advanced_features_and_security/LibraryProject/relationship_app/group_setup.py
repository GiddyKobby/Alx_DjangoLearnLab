from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

def create_default_groups():
    book_content_type = ContentType.objects.get_for_model(Book)

    # Fetch permissions
    can_view = Permission.objects.get(codename="can_view", content_type=book_content_type)
    can_create = Permission.objects.get(codename="can_create", content_type=book_content_type)
    can_edit = Permission.objects.get(codename="can_edit", content_type=book_content_type)
    can_delete = Permission.objects.get(codename="can_delete", content_type=book_content_type)

    # Create Groups
    editors, _ = Group.objects.get_or_create(name="Editors")
    viewers, _ = Group.objects.get_or_create(name="Viewers")
    admins, _ = Group.objects.get_or_create(name="Admins")

    # Assign permissions
    viewers.permissions.set([can_view])
    editors.permissions.set([can_view, can_create, can_edit])
    admins.permissions.set([can_view, can_create, can_edit, can_delete])
