from django.contrib.auth.models import Group, Permission
from warehouse.models import Location, Container, Inventory, MovementHistory
from django.contrib.contenttypes.models import ContentType

# Create groups
clerk_group, _ = Group.objects.get_or_create(name='Warehouse Clerk')
supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
manager_group, _ = Group.objects.get_or_create(name='Manager')

# Define permissions
location_ct = ContentType.objects.get_for_model(Location)
container_ct = ContentType.objects.get_for_model(Container)
inventory_ct = ContentType.objects.get_for_model(Inventory)
movement_ct = ContentType.objects.get_for_model(MovementHistory)

# Clerk permissions: create containers, add movements
clerk_permissions = [
    Permission.objects.get(codename='add_container', content_type=container_ct),
    Permission.objects.get(codename='add_movementhistory', content_type=movement_ct),
]

clerk_group.permissions.set(clerk_permissions)

# Supervisor permissions: clerk perms + create locations
supervisor_permissions = clerk_permissions + [
    Permission.objects.get(codename='add_location', content_type=location_ct),
]

supervisor_group.permissions.set(supervisor_permissions)

# Manager permissions: all model permissions
manager_permissions = Permission.objects.filter(content_type__in=[
    location_ct, container_ct, inventory_ct, movement_ct
])
manager_group.permissions.set(manager_permissions)

print("Groups and permissions set successfully.")

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from warehouse.models import Inventory, InventoryAdjustment  # Ensure InventoryAdjustment is imported

# Create the groups
inventory_manager_group, _ = Group.objects.get_or_create(name='Inventory Manager')
inventory_counter_group, _ = Group.objects.get_or_create(name='Inventory Counter')

# Get content types
inventory_ct = ContentType.objects.get_for_model(Inventory)
adjustment_ct = ContentType.objects.get_for_model(InventoryAdjustment)

# Define permissions for Inventory Manager:
# Allow full CRUD on Inventory and full management of InventoryAdjustment
manager_inventory_perms = Permission.objects.filter(
    content_type=inventory_ct, codename__in=['add_inventory', 'change_inventory', 'delete_inventory']
)
manager_adjustment_perms = Permission.objects.filter(
    content_type=adjustment_ct  # Assuming add, change, and delete exist by default
)
inventory_manager_group.permissions.set(list(manager_inventory_perms) + list(manager_adjustment_perms))

# Define permissions for Inventory Counter:
# Limited to updating (cycle count) Inventory and adding/changing adjustments (but not deleting)
counter_inventory_perms = Permission.objects.filter(
    content_type=inventory_ct, codename__in=['change_inventory']
)
counter_adjustment_perms = Permission.objects.filter(
    content_type=adjustment_ct, codename__in=['add_inventoryadjustment', 'change_inventoryadjustment']
)
inventory_counter_group.permissions.set(list(counter_inventory_perms) + list(counter_adjustment_perms))

print("Inventory control groups and permissions set successfully.")
