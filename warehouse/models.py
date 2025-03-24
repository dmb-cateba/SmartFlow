from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Product(models.Model):
    """
    Represents a product (master data).
    """
    UNIT_TYPES = [
        ('PCS', 'Pieces'),
        ('KG', 'Kilograms'),
        ('LBS', 'Pounds'),
        ('M', 'Meters'),
        ('CM', 'Centimeters'),
        ('MM', 'Millimeters'),
        ('IN', 'Inches'),
        ('FT', 'Feet'),
        ('YD', 'Yards'),
        ('GAL', 'Gallons'),
        ('LT', 'Liters'),
        # Add more as needed.
    ]

    whseSKU = models.CharField(max_length=50, unique=True, primary_key=True)  # Unique Warehouse SKU
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit_type = models.CharField(max_length=5, choices=UNIT_TYPES, blank=True, null=True)  # e.g., PCS, KG, LBS
    #add vendor sku
    vendorSKU = models.CharField(max_length=255, blank=True, null=True)
    # Add other relevant product attributes here (e.g., category, brand, etc.)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.whseSKU} - {self.name}"

    def clean(self):
        """
        Custom validation to ensure that at least one of width, length, height,
        weight, or unit_type is provided, and that if weight is provided,
        unit_type is also provided (and vice versa).  Also checks for negative
        dimensions and weight.
        """
        if not any([self.width, self.length, self.height, self.weight, self.unit_type]):
            raise ValidationError("At least one of width, length, height, weight, or unit_type must be provided.")

        if (self.weight is not None and self.unit_type is None) or (self.weight is None and self.unit_type is not None and self.unit_type in ['KG','LBS']):
             raise ValidationError("If weight is provided, unit_type (KG or LBS) must also be provided, and vice versa.")
        #check that weight is provided if unit type is kgs or lbs
        if (self.unit_type in ['KG', 'LBS'] and self.weight is None):
            raise ValidationError("If unit type is KG or LBS, weight must be provided.")
        #check that if unit type is not kg or lbs weight should be null
        if (self.unit_type not in  ['KG', 'LBS']  and self.weight is not None ):
            raise ValidationError("Unit type should be KG or LBS if weight is provided.")

        # Check for negative dimensions or weight
        if (self.width is not None and self.width < 0) or \
           (self.length is not None and self.length < 0) or \
           (self.height is not None and self.height < 0) or \
           (self.weight is not None and self.weight < 0):
            raise ValidationError("Dimensions and weight cannot be negative.")



class Location(models.Model):
    LOCATION_TYPES = [
        ('BIN', 'Bin'),
        ('STG_IN', 'Pallet Staging Inbound'),
        ('STG_OUT', 'Pallet Staging Outbound'),
        ('RECEIVING', 'Receiving'),
        ('SHIPPING', 'Shipping'),
        ('DROP_ZONE', 'Drop Zone'),
        ('CART', 'Cart'),
        ('PALLETIZE', 'Palletize Area'),
        ('PROBLEM_SOLVING', 'Problem Solving Area'),
        ('QUARANTINE', 'Quarantine'),
        ('DAMAGED', 'Damaged'),
        ('PICKING', 'Picking'),
        ('PACKING', 'Packing'),
        ('RETURNS_AREA', 'returns area'),#newly added
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('BLOCKED', 'Blocked'),
        ('RESERVED', 'Reserved'),
    ]

    location_id = models.CharField(max_length=255, primary_key=True)  # e.g., WH-A-01-R02-S03-B04
    warehouse_id = models.CharField(max_length=255)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPES)
    capacity_weight = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # in kgs
    capacity_volume = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # in cubic units
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='AVAILABLE')
    item_restrictions = models.TextField(blank=True, null=True)
    accessibility_priority = models.IntegerField(default=0)
    coordinates_x = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coordinates_y = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coordinates_z = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.location_id} - {self.get_location_type_display()}"

class Container(models.Model):
    CONTAINER_TYPES = [
        ('PALLET', 'Pallet'),
        ('BOX', 'Box'),
        ('CASE', 'Case'),
    ]

    barcode = models.CharField(max_length=255, primary_key=True)
    container_type = models.CharField(max_length=50, choices=CONTAINER_TYPES)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.barcode} ({self.get_container_type_display()})"

class Inventory(models.Model):
    # Link to Product using whseSKU
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory_items", db_column='whseSKU')
    #removed barcode
    barcode = models.CharField(max_length=255, primary_key=True) #added primary key, should not be duplicated
    #name and description no needed, get them from master data
    # name = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.barcode} - {self.product.name}" #use product name instead of name



class MovementHistory(models.Model):
    MOVEMENT_REASON_CHOICES = [
        ('INBOUND_STAGING', 'Inbound Staging'),
        ('OUTBOUND_STAGING', 'Outbound Staging'),
        ('PALLETIZATION', 'Palletization'),
        ('PROBLEM_SOLVING', 'Problem Solving'),
        ('TRUCK_LOADING', 'Truck Loading'),
        ('TRUCK_UNLOADING', 'Truck Unloading'),
        ('RETURNS', 'Returns'),
        ('CROSS_DOCK_UNLOADING', 'CROSS_DOCK_UNLOADING'),
        ('CROSS_DOCK_STAGING', 'CROSS_DOCK_STAGING'),
        ('INVENTORY_MOVEMENT','INVENTORY_MOVEMENT'),
        ('PICKING','PICKING'),
        ('STOWING','STOWING'),
        # case returns undelivered
        # create returns location
    ]

    # Use ForeignKey to link to Inventory
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="movement_history")
    #item barcode not needed, get it from iventory item
    #item_barcode = models.CharField(max_length=255)
    # Foreign Keys instead of CharFields for locations and containers
    from_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="movements_from")
    to_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="movements_to")
    from_container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True, blank=True, related_name="movements_from")
    to_container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True, blank=True, related_name="movements_to")

    movement_reason = models.CharField(
        max_length=50,
        choices=MOVEMENT_REASON_CHOICES,
        blank=True,
        null=True
    )
    event_time = models.DateTimeField(auto_now_add=True)
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     #add whsesku for tracking sku movement as well
    whseSKU = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="product_movements")

    def __str__(self):
        return (f"Item {self.inventory_item.barcode} ({self.inventory_item.product.whseSKU}) moved from "
                f"{self.from_location or self.from_container} to {self.to_location or self.to_container} "
                f"on {self.event_time.strftime('%Y-%m-%d %H:%M:%S')} by {self.moved_by}")

    def save(self, *args, **kwargs):
        # Set the whseSKU based on the inventory_item
        if self.inventory_item:
            self.whseSKU = self.inventory_item.product
        super().save(*args, **kwargs)

class InventoryAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('ADD', 'Addition'),
        ('REMOVE', 'Removal'),
    ]
    
    # Auto-generated primary key (or you can use UUID if preferred)
    adjustment_id = models.AutoField(primary_key=True)
    
    # Link the adjustment to an inventory item
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    
    # Optional fields for location transitions (could be null if not applicable)
    from_location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='adjustment_from'
    )
    to_location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='adjustment_to'
    )
    
    quantity = models.PositiveIntegerField()
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    reason = models.TextField()
    
    # Track who made the adjustment
    adjusted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjustment {self.adjustment_id} for {self.inventory_item}"

"""
from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    LOCATION_TYPES = [
        ('BIN', 'Bin'),
        ('STG_IN', 'Pallet Staging Inbound'),
        ('STG_OUT', 'Pallet Staging Outbound'),
        ('RECEIVING', 'Receiving'),
        ('SHIPPING', 'Shipping'),
        ('DROP_ZONE', 'Drop Zone'),
        ('CART', 'Cart'),
        ('PALLETIZE', 'Palletize Area'),
        ('PROBLEM_SOLVING', 'Problem Solving Area'),
        ('QUARANTINE', 'Quarantine'),
        ('DAMAGED', 'Damaged'),
        ('PICKING', 'Picking'),
        ('PACKING', 'Packing'),
        ('RETURNS_AREA', 'returns area'),#newly added
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('BLOCKED', 'Blocked'),
        ('RESERVED', 'Reserved'),
    ]

    location_id = models.CharField(max_length=255, primary_key=True)  # e.g., WH-A-01-R02-S03-B04
    warehouse_id = models.CharField(max_length=255)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPES)
    capacity_weight = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # in kgs
    capacity_volume = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # in cubic units
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='AVAILABLE')
    item_restrictions = models.TextField(blank=True, null=True)
    accessibility_priority = models.IntegerField(default=0)
    coordinates_x = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coordinates_y = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coordinates_z = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.location_id} - {self.get_location_type_display()}"

class Container(models.Model):
    CONTAINER_TYPES = [
        ('PALLET', 'Pallet'),
        ('BOX', 'Box'),
        ('CASE', 'Case'),
    ]

    barcode = models.CharField(max_length=255, primary_key=True)
    container_type = models.CharField(max_length=50, choices=CONTAINER_TYPES)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.barcode} ({self.get_container_type_display()})"

class Inventory(models.Model):
    barcode = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.barcode} - {self.name}"

class MovementHistory(models.Model):
    MOVEMENT_REASON_CHOICES = [
        ('INBOUND_STAGING', 'Inbound Staging'),
        ('OUTBOUND_STAGING', 'Outbound Staging'),
        ('PALLETIZATION', 'Palletization'),
        ('PROBLEM_SOLVING', 'Problem Solving'),
        ('TRUCK_LOADING', 'Truck Loading'),
        ('TRUCK_UNLOADING', 'Truck Unloading'),
        ('RETURNS', 'Returns'),
        ('CROSS_DOCK_UNLOADING', 'CROSS_DOCK_UNLOADING'),
        ('CROSS_DOCK_STAGING', 'CROSS_DOCK_STAGING'),
        ('INVENTORY_MOVEMENT','INVENTORY_MOVEMENT'),
        ('PICKING','PICKING'),
        ('STOWING','STOWING'),
        # case returns undelivered
        # create returns location
    ]

    item_barcode = models.CharField(max_length=255)
    from_location = models.CharField(max_length=255, blank=True, null=True)
    to_location = models.CharField(max_length=255, blank=True, null=True)
    from_container = models.CharField(max_length=255, blank=True, null=True)
    to_container = models.CharField(max_length=255, blank=True, null=True)
    movement_reason = models.CharField(
        max_length=50, 
        choices=MOVEMENT_REASON_CHOICES, 
        blank=True, 
        null=True
    )
    event_time = models.DateTimeField(auto_now_add=True)
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (f"Item {self.item_barcode} moved from "
                f"{self.from_location or self.from_container} to {self.to_location or self.to_container} "
                f"on {self.event_time.strftime('%Y-%m-%d %H:%M:%S')} by {self.moved_by}")
    
class InventoryAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('ADD', 'Addition'),
        ('REMOVE', 'Removal'),
    ]
    
    # Auto-generated primary key (or you can use UUID if preferred)
    adjustment_id = models.AutoField(primary_key=True)
    
    # Link the adjustment to an inventory item
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    
    # Optional fields for location transitions (could be null if not applicable)
    from_location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='adjustment_from'
    )
    to_location = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='adjustment_to'
    )
    
    quantity = models.PositiveIntegerField()
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    reason = models.TextField()
    
    # Track who made the adjustment
    adjusted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjustment {self.adjustment_id} for {self.inventory_item}"

"""