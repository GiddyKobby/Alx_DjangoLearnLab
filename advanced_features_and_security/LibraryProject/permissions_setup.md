# Django Permissions & Groups Setup

## Custom Permissions
Defined in `relationship_app/models.py` inside the `Book` model:

- can_view
- can_create
- can_edit
- can_delete

## Groups Created
Groups defined in `relationship_app/group_setup.py`:

- **Viewers** → can_view
- **Editors** → can_view, can_create, can_edit
- **Admins** → all permissions

Run group setup:

```bash
python manage.py shell
>>> from relationship_app.group_setup import create_default_groups
>>> create_default_groups()
