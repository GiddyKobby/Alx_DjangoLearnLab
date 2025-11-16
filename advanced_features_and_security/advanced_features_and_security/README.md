# Permissions & Groups Setup

## Custom Permissions
Defined in Article model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
### Viewers
- can_view

### Editors
- can_view
- can_create
- can_edit

### Admins
- All permissions

## How It Works
Views use @permission_required to check permissions before allowing:
- Viewing articles
- Creating articles
- Editing articles
- Deleting articles

## Testing
Create test users in Django Admin and assign them to groups.
Each user will only be able to perform the actions that match their group permissions.
