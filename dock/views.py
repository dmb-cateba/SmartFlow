from django.shortcuts import render

def dock_view(request):
    # Sample static data for demonstration.
    inbound_loads = [
        {
            'Dock_Door': 'DD10',
            'trailer_id': 'TRL-101',
            'carrier': 'DMB',
            'voyage/load_id': 'VY-2023-001',
            'lane': 'QUE01->MAS01',
            'ETA': '10:00',
            'AAT': '11:15',
            'Unload_start': '11:25',
            'Unload_complete': '',
            'completion': 75,
            'status':'loading_in_progress',
            'release_time':'',
        },
        {
            'Dock_Door': 'DD07',
            'trailer_id': 'TRL-102',
            'carrier': 'TLP',
            'voyage/load_id': 'VY-2023-002',
            'lane': 'TLP01->MAS01',
            'ETA': '09:00',
            'AAT': '09:05',
            'Unload_start': '09:10',
            'Unload_complete': '09:45',
            'completion': 100,
            'status':'unloading_complete',
            'release_time':'10:00',
        },
    ]
    
    outbound_loads = [

        {
            'Dock_Door': 'DD010',
            'load_id': 'LD-2023-044',
            'trailer_id': 'TRL-101',
            'carrier': 'DMB',
            'lane':'MAS01->Retail-101/150',
            'route':'101-150',
            'Trailer Ready Time': '02:00',
            'ETD': '03:00',
            'ADT': '04:15',
            'loading_start': '01:25',
            'loading_complete': '02:00',
            'completion': 100,
            'status':'departed',
            'release_time':'02:15',
        },
        {
            'Dock_Door': 'DD004',
            'load_id': 'LD-2023-045',
            'trailer_id': 'TRL-101',
            'carrier': 'DMB',
            'lane':'MAS01->Retail-101/150',
            'route':'101-150',
            'Trailer Ready Time': '11:00',
            'ETD': '14:00',
            'ADT': '',
            'loading_start': '13:25',
            'loading_complete': '',
            'completion': 90,
            'status':'loading_in_progress',
            'release_time':'',
        },
    ]
    
    context = {
        'inbound_loads': inbound_loads,
        'outbound_loads': outbound_loads,
    }
    return render(request, 'dock/dock.html', context)
