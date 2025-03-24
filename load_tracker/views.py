from django.shortcuts import render

def index(request):
    # Sample data for load tracking
    loads = [
        {
            'load_voyage_number': 'LV1001',
            'lane_from': 'Warehouse A',
            'lane_to': 'Customer X',
            'load_type': 'Outbound',
            'first_facility_eta': '2025-03-24 12:00',
            'first_facility_arrival_status': 'Yes (2025-03-24 12:05)',
            'first_facility_departure_status': 'Yes (2025-03-24 12:20)',
            'next_facility_eta': '2025-03-24 15:00',
            'next_facility_arrival_status': 'No',
            'next_facility_departure_status': 'N/A',
            'final_destination_arrival_status': 'No',
            'customers_suppliers': 'Customer X',
        },
        {
            'load_voyage_number': 'LV1002',
            'lane_from': 'Warehouse A',
            'lane_to': 'Customer Y',
            'load_type': 'Outbound',
            'first_facility_eta': '2025-03-24 10:00',
            'first_facility_arrival_status': 'Yes (2025-03-24 10:05)',
            'first_facility_departure_status': 'Yes (2025-03-24 10:15)',
            'next_facility_eta': '2025-03-24 13:00',
            'next_facility_arrival_status': 'Yes (2025-03-24 13:05)',
            'next_facility_departure_status': 'Yes (2025-03-24 13:20)',
            'final_destination_arrival_status': 'Yes (2025-03-24 16:00)',
            'customers_suppliers': 'Customer Y',
        },
        {
            'load_voyage_number': 'LV2001',
            'lane_from': 'Warehouse A',
            'lane_to': 'Supplier Z',
            'load_type': 'Inbound',
            'first_facility_eta': '2025-03-25 08:00',
            'first_facility_arrival_status': 'No',
            'first_facility_departure_status': 'N/A',
            'next_facility_eta': 'N/A',
            'next_facility_arrival_status': 'N/A',
            'next_facility_departure_status': 'N/A',
            'final_destination_arrival_status': 'No',
            'customers_suppliers': 'Supplier Z',
        },
    ]

    # Summary data for landing page charts
    summary = {
        'loads_in_transit': 2,
        'loads_completed': 1,
        'status_breakdown': {
            'departed_warehouse': 0,
            'arrived_first_facility': 2,
            'in_transit_next_facility': 1,
            'completed': 1,
        }
    }

    context = {
        'loads': loads,
        'summary': summary,
    }
    return render(request, 'load_tracker/load_tracker.html', context)
