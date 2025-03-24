# troubleshooting/views.py
from django.shortcuts import render

def index(request):
    # Sample data for movement history transactions
    movement_history = [
        {
            'timestamp': '2025-03-22 08:30',
            'transaction_type': 'Receive Inventory',
            'whs_esku': 'WHS1001',
            'vendor_sku': 'VEND2001',
            'container': 'PALLET001',
            'quantity': 100,
            'location_before': 'Dock',
            'location_after': 'Receiving Area',
            'user': 'User123',
            'reference_document': 'PO12345',
        },
        {
            'timestamp': '2025-03-22 09:00',
            'transaction_type': 'Put Away',
            'whs_esku': 'WHS1001',
            'vendor_sku': 'VEND2001',
            'container': 'PALLET001',
            'quantity': 100,
            'location_before': 'Receiving Area',
            'location_after': 'Bin A1',
            'user': 'User456',
            'reference_document': 'PO12345',
        },
        {
            'timestamp': '2025-03-23 10:15',
            'transaction_type': 'Pick',
            'whs_esku': 'WHS1002',
            'vendor_sku': 'VEND2002',
            'container': '',
            'quantity': 50,
            'location_before': 'Bin B2',
            'location_after': 'Staging Area',
            'user': 'User789',
            'reference_document': 'SO54321',
        },
    ]
    
    # Capture search parameters from GET request (for demonstration purposes)
    search_id = request.GET.get('search_id', '')
    input_type = request.GET.get('input_type', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    # In a complete implementation, you'd filter 'movement_history' based on the search parameters.
    context = {
        'movement_history': movement_history,
        'search_id': search_id,
        'input_type': input_type,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'troubleshooting/troubleshooting.html', context)
