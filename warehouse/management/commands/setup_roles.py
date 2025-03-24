from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from warehouse.models import Location, Container, Inventory, MovementHistory, InventoryAdjustment

class Command(BaseCommand):
    help = "Setup roles and permissions for warehouse management"

    def handle(self, *args, **kwargs):
        # Create Groups
        clerk_group, _ = Group.objects.get_or_create(name='Warehouse Clerk')
        supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        inventory_manager_group, _ = Group.objects.get_or_create(name='Inventory Manager')
        inventory_counter_group, _ = Group.objects.get_or_create(name='Inventory Counter')

        # Content Types
        location_ct = ContentType.objects.get_for_model(Location)
        container_ct = ContentType.objects.get_for_model(Container)
        inventory_ct = ContentType.objects.get_for_model(Inventory)
        movement_ct = ContentType.objects.get_for_model(MovementHistory)
        adjustment_ct = ContentType.objects.get_for_model(InventoryAdjustment)

        # Warehouse Clerk Permissions
        clerk_permissions = [
            Permission.objects.get(codename='add_container', content_type=container_ct),
            Permission.objects.get(codename='add_movementhistory', content_type=ContentType.objects.get_for_model(MovementHistory)),
        ]
        clerk_group.permissions.set(clerk_permissions := clerk_permissions)

        # Supervisor Permissions (Clerk permissions + create locations)
        supervisor_permissions = clerk_permissions + [
            Permission.objects.get(codename='add_location', content_type=location_ct),
        ]
        supervisor_group.permissions.set(supervisor_permissions)

        # Manager Permissions: Full administrative permissions on core models
        manager_permissions = Permission.objects.filter(
            content_type__in=[location_ct, container_ct, inventory_ct, ContentType.objects.get_for_model(MovementHistory)]
        )
        manager_group.permissions.set(manager_permissions)

        # Inventory Manager Permissions: Full CRUD on Inventory & InventoryAdjustment
        manager_inventory_perms = Permission.objects.filter(
            content_type=inventory_ct,
            codename__in=['add_inventory', 'change_inventory', 'delete_inventory']
        )
        manager_adjustment_perms = Permission.objects.filter(content_type=ContentType.objects.get_for_model(InventoryAdjustment))
        inventory_manager_group.permissions.set(list(manager_inventory_perms) + list(manager_adjustment_perms))

        # Inventory Counter Permissions: Limited (no delete)
        counter_inventory_perms = Permission.objects.filter(
            content_type=inventory_ct, 
            codename__in=['change_inventory']
        )
        counter_adjustment_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(InventoryAdjustment),
            codename__in=['add_inventoryadjustment', 'change_inventoryadjustment']
        )
        inventory_counter_group.permissions.set(list(counter_inventory_perms) + list(counter_adjustment_perms))

        self.stdout.write(self.style.SUCCESS("✅ Inventory control groups and permissions set successfully."))
