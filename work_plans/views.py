from django.shortcuts import render

def index(request):
    inbound_work_plans = [
        {
            'eta': '2025-03-24 09:00',
            'truck_number': 'TRK1234',
            'lane': 'Supplier A',
            'load_type': 'Inbound Supplier',
            'sku': 'SKU001',
            'description': 'Widgets Type A',
            'container': 'PALLET001',
            'quantity': 100,
            'expected_reception_date': '2025-03-24',
            'store_by_date': '2025-03-25',  # Relevant for standard inbound
            'stage_by_date': '',            # Not applicable for standard inbound
            'status': 'Pending Arrival'
        },
        {
            'eta': '2025-03-25 11:00',
            'truck_number': 'TRK5678',
            'lane': 'Facility B',
            'load_type': 'Cross Dock',
            'sku': 'SKU002',
            'description': 'Gadgets Type B',
            'container': 'PALLET002',
            'quantity': 50,
            'expected_reception_date': '2025-03-25',
            'store_by_date': '',            # Not applicable for cross dock
            'stage_by_date': '2025-03-25',    # Relevant for cross dock shipments
            'status': 'Arrived'
        },
    ]
    
    # Work Completion Summary for Inbound View (e.g., aggregated over today, tomorrow, and day after)
    work_completion_summary = {
        'today': {'expected': 150, 'received': 90},
        'tomorrow': {'expected': 200, 'received': 120},
        'day_after': {'expected': 180, 'received': 60},
    }

    # Generic sample data for Outbound Work Plans
    outbound_work_plans = [
        {
            'scheduled_departure': '2025-03-26 14:00',
            'load_id': 'LOAD1001',
            'route': 'Destination A',
            'load_type': 'Outbound Shipment to Customer',
            'sku': 'SKU003',
            'description': 'Widgets Type C',
            'quantity': 75,
            'current_location': 'Inventory - Bin A1',
            'dock_door': 'Door 1',
            'status': 'Pending Picking',
        },
        {
            'scheduled_departure': '2025-03-26 15:00',
            'load_id': 'LOAD1002',
            'route': 'Destination B',
            'load_type': 'Cross Dock to Outbound',
            'sku': 'SKU004',
            'description': 'Gadgets Type D',
            'quantity': 60,
            'current_location': 'Picking in Progress',
            'dock_door': 'Door 2',
            'status': 'Picking',
        },
        {
            'scheduled_departure': '2025-03-26 16:00',
            'load_id': 'LOAD1003',
            'route': 'Destination C',
            'load_type': 'Intercompany Transfer',
            'sku': 'SKU005',
            'description': 'Device Type E',
            'quantity': 30,
            'current_location': 'Staging',
            'dock_door': 'Door 3',
            'status': 'Staged',
        },
        {
            'scheduled_departure': '2025-03-26 17:00',
            'load_id': 'LOAD1004',
            'route': 'Destination D',
            'load_type': 'Outbound Shipment to Customer',
            'sku': 'SKU006',
            'description': 'Device Type F',
            'quantity': 45,
            'current_location': 'Loading',
            'dock_door': 'Door 4',
            'status': 'Loading',
        },
    ]

    context = {
        'inbound_work_plans': inbound_work_plans,
        'outbound_work_plans': outbound_work_plans,
        'work_completion_summary': work_completion_summary,
    }
    return render(request, 'work_plans/work_plans.html', context)
