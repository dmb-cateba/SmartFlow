from django.contrib import admin
from .models import Location, Container, Inventory, MovementHistory
from django.contrib import admin
from .models import InventoryAdjustment

# Base class for role-based permission handling
class RoleBasedAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name__in=['Manager', 'Supervisor']).exists()

    def has_add_permission(self, request):
        return request.user.groups.filter(name__in=['Warehouse Clerk', 'Supervisor', 'Manager']).exists()

# Admin for Location with detailed view
@admin.register(Location)
class LocationAdmin(RoleBasedAdmin):
    list_display = ('location_id', 'location_type', 'status', 'capacity_weight', 'capacity_volume', 'accessibility_priority', 'warehouse_id')
    list_filter = ('location_type', 'status', 'warehouse_id')
    search_fields = ('location_id', 'warehouse_id', 'location_type', 'item_restrictions')
    list_editable = ('status', 'accessibility_priority')
    ordering = ('warehouse_id', 'location_type', 'accessibility_priority')

# Admin for Container
@admin.register(Container)
class ContainerAdmin(RoleBasedAdmin):
    list_display = ('barcode', 'container_type', 'status', 'current_location', 'updated_at')
    list_filter = ('container_type', 'status')
    search_fields = ('barcode',)
    list_editable = ('status', 'current_location')
    ordering = ('-updated_at',)

# Admin for Inventory
@admin.register(Inventory)
class InventoryAdmin(RoleBasedAdmin):
    list_display = ('barcode', 'get_product_name', 'quantity', 'expiry_date', 'current_location', 'container', 'date_modified')
    list_filter = ('expiry_date', 'current_location', 'container')
    search_fields = ('barcode', 'product__name', 'product__description')
    list_editable = ('quantity', 'current_location', 'container')
    ordering = ('expiry_date', 'quantity')
    
    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = "Product Name"


# Admin for MovementHistory with stricter permissions
@admin.register(MovementHistory)
class MovementHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'whseSKU', 
        'movement_reason',
        'from_location', 
        'to_location', 
        'from_container', 
        'to_container', 
        'event_time', 
        'moved_by'
    )
    list_filter = ('movement_reason', 'event_time', 'moved_by', 'from_location', 'to_location')
    search_fields = ('whseSKU', 'from_location', 'to_location', 'from_container', 'to_container')
    readonly_fields = (
        'whseSKU', 
        'from_location', 
        'to_location', 
        'from_container', 
        'to_container', 
        'event_time', 
        'moved_by',
        'movement_reason'
    )
    ordering = ('-event_time',)

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists()

    def has_add_permission(self, request):
        return request.user.groups.filter(name__in=['Warehouse Clerk', 'Supervisor', 'Manager']).exists()

    def has_change_permission(self, request, obj=None):
        return False  # Movement history should remain immutable once recorded

class InventoryAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('adjustment_id', 'inventory_item', 'adjustment_type', 'quantity', 'timestamp', 'adjusted_by')
    search_fields = ('inventory_whseSKU', 'reason')
    list_filter = ('adjustment_type', 'timestamp')
    
    def has_delete_permission(self, request, obj=None):
        # Only Inventory Managers should be able to delete adjustments.
        return request.user.groups.filter(name='Inventory Manager').exists()

    def has_change_permission(self, request, obj=None):
        # Inventory Managers can change; Inventory Counters might be limited to adding or viewing.
        return request.user.groups.filter(name__in=['Inventory Manager', 'Inventory Counter']).exists()

    def has_add_permission(self, request):
        # Both roles can add adjustments, but deletion is restricted.
        return request.user.groups.filter(name__in=['Inventory Manager', 'Inventory Counter']).exists()

admin.site.register(InventoryAdjustment, InventoryAdjustmentAdmin)
