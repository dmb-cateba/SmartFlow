# inventory/views.py
from django.shortcuts import render

def index(request):
    inventory_items = [
        {
            'whs_esku': 'WHS1001',
            'vendor_sku': 'VEND2001',
            'description': 'Widget A - Standard Model',
            'bin_number': 'A1',
            'expiration_date': '2025-06-30',
            'reception_date': '2025-03-20',
            'supplier': 'Supplier X',
            'last_movement_by': 'User123',
            'last_movement_on': '2025-03-22 14:30',
            'quantity': 150,
        },
        {
            'whs_esku': 'WHS1002',
            'vendor_sku': 'VEND2002',
            'description': 'Gadget B - Premium Model',
            'bin_number': 'B2',
            'expiration_date': '',
            'reception_date': '2025-03-21',
            'supplier': 'Supplier Y',
            'last_movement_by': 'User456',
            'last_movement_on': '2025-03-23 10:15',
            'quantity': 80,
        },
        {
            'whs_esku': 'WHS1003',
            'vendor_sku': 'VEND2003',
            'description': 'Device C - Compact',
            'bin_number': 'C3',
            'expiration_date': '2025-04-15',
            'reception_date': '2025-03-19',
            'supplier': 'Supplier Z',
            'last_movement_by': 'User789',
            'last_movement_on': '2025-03-20 09:45',
            'quantity': 200,
        },
    ]
    context = {'inventory_items': inventory_items}
    return render(request, 'inventory/inventory_list.html', context)

def inventory_metrics(request):
    # Sample metrics data
    metrics = {
        'inventory_turnover_rate': 5.6,
        'days_of_supply': 12,
        'fill_rate': '98%',
        'stockout_rate': '2%',
        'carrying_cost': '$1500',
        'average_inventory_level': 180,
        'order_cycle_time': '3 days',
    }
    context = {'metrics': metrics}
    return render(request, 'inventory/inventory_metrics.html', context)
