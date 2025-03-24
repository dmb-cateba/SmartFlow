# populate_data.py
from decimal import Decimal
from datetime import date
from django.contrib.auth.models import User
from warehouse.models import Product, Location, Container, Inventory, MovementHistory, InventoryAdjustment

def populate():
    # Create a test user (if not already present)
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass')
        user.save()
        print("Test user created.")
    else:
        print("Test user already exists.")

    # Create Products
    product1, created = Product.objects.get_or_create(
        whseSKU="SKU001",
        defaults={
            'name': "Widget",
            'description': "A useful widget",
            'width': Decimal("10.00"),
            'length': Decimal("5.00"),
            'height': Decimal("2.00"),
            'unit_type': "PCS",  # non-weight based unit
        }
    )
    if created:
        print("Product SKU001 created.")
    else:
        print("Product SKU001 already exists.")

    product2, created = Product.objects.get_or_create(
        whseSKU="SKU002",
        defaults={
            'name': "Gadget",
            'description': "A fancy gadget",
            'width': Decimal("15.00"),
            'length': Decimal("7.50"),
            'height': Decimal("3.00"),
            'weight': Decimal("2.50"),
            'unit_type': "KG",  # weight-based unit
        }
    )
    if created:
        print("Product SKU002 created.")
    else:
        print("Product SKU002 already exists.")

    # Create Locations
    location1, created = Location.objects.get_or_create(
        location_id="BIN001",
        defaults={
            'warehouse_id': "WH1",
            'location_type': "BIN",
            'capacity_weight': Decimal("10000.00"),
            'capacity_volume': Decimal("10000.00"),
            'length': Decimal("100.00"),
            'width': Decimal("100.00"),
            'height': Decimal("50.00"),
            'status': "AVAILABLE",
        }
    )
    if created:
        print("Location BIN001 created.")
    else:
        print("Location BIN001 already exists.")

    location2, created = Location.objects.get_or_create(
        location_id="STG_IN001",
        defaults={
            'warehouse_id': "WH1",
            'location_type': "STG_IN",
            'capacity_weight': Decimal("5000.00"),
            'capacity_volume': Decimal("5000.00"),
            'length': Decimal("80.00"),
            'width': Decimal("80.00"),
            'height': Decimal("40.00"),
            'status': "AVAILABLE",
        }
    )
    if created:
        print("Location STG_IN001 created.")
    else:
        print("Location STG_IN001 already exists.")

    location3, created = Location.objects.get_or_create(
        location_id="DROPZONE_UNKNOWN",
        defaults={
            'warehouse_id': "WH1",
            'location_type': "DROP_ZONE",
            'capacity_weight': Decimal("10000.00"),
            'capacity_volume': Decimal("10000.00"),
            'length': Decimal("50.00"),
            'width': Decimal("50.00"),
            'height': Decimal("20.00"),
            'status': "AVAILABLE",
        }
    )
    if created:
        print("Location DROPZONE_UNKNOWN created.")
    else:
        print("Location DROPZONE_UNKNOWN already exists.")

    # Create Containers
    container1, created = Container.objects.get_or_create(
        barcode="CONT001",
        defaults={
            'container_type': "PALLET",
            'current_location': location1,
            'status': "ACTIVE",
        }
    )
    if created:
        print("Container CONT001 created.")
    else:
        print("Container CONT001 already exists.")

    container2, created = Container.objects.get_or_create(
        barcode="CONT002",
        defaults={
            'container_type': "BOX",
            'current_location': location2,
            'status': "ACTIVE",
        }
    )
    if created:
        print("Container CONT002 created.")
    else:
        print("Container CONT002 already exists.")

    # Create Inventory Items
    inventory1, created = Inventory.objects.get_or_create(
        barcode="INV001",
        defaults={
            'product': product1,
            'quantity': 50,
            'expiry_date': date(2025, 12, 31),
            'current_location': location1,
            'container': container1,
        }
    )
    if created:
        print("Inventory INV001 created.")
    else:
        print("Inventory INV001 already exists.")

    inventory2, created = Inventory.objects.get_or_create(
        barcode="INV002",
        defaults={
            'product': product2,
            'quantity': 30,
            'expiry_date': date(2026, 6, 30),
            'current_location': location2,
            'container': container2,
        }
    )
    if created:
        print("Inventory INV002 created.")
    else:
        print("Inventory INV002 already exists.")

    # Create a sample MovementHistory record
    movement, created = MovementHistory.objects.get_or_create(
        inventory_item=inventory1,
        from_location=location2,
        to_location=location1,
        movement_reason="INBOUND_STAGING",
        moved_by=user,
    )
    if created:
        print("Sample movement history created.")
    else:
        print("Sample movement history already exists.")

    print("Basic data populated.")

if __name__ == "__main__":
    populate()
