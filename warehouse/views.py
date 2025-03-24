from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .forms import LocationForm, ContainerForm
from .models import Location, Container, Inventory, MovementHistory, Product
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Product  # Import your Product model
import json
from django.core.exceptions import BadRequest

def scanner_view(request):
    return render(request, 'warehouse/test_gpt.html', {})  # scannerui3

# Location views
@login_required
@permission_required('warehouse.add_location', raise_exception=True)
def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location-list')
    else:
        form = LocationForm()
    return render(request, 'warehouse/create_location.html', {'form': form})

@csrf_exempt  # Use csrf_exempt for simplicity in this example.  In production, use proper CSRF protection.
def product_exists(request):
    """
    Checks if a product exists based on whseSKU or vendorSKU.

    Receives a POST request with an 'item_id' in the body.

    Returns:
        JsonResponse:  { "exists": true } if the product exists,
                       { "exists": false } if it doesn't.
                       { "error": "message" } if there's an error.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.  Use POST.'}, status=405)  # 405 Method Not Allowed

    try:
        # Attempt to parse JSON data from the request body
        data = json.loads(request.body)
        item_id = data.get('item_id')

        if not item_id:
            return JsonResponse({'error': 'Missing item_id in request body.'}, status=400)  # 400 Bad Request

        # Check if the item_id exists as either whseSKU or vendorSKU
        exists = Product.objects.filter(whseSKU=item_id).exists() or \
                 Product.objects.filter(vendorSKU=item_id).exists()

        return JsonResponse({'exists': exists})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data in request body.'}, status=400)  # 400 Bad Request
    except BadRequest as e:
        return JsonResponse({'error': str(e)},status=400)
    except Exception as e:
        # Catch any other unexpected errors
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)  # 500 Internal Server Error



@login_required
@csrf_exempt
def location_detail(request):
    """
    Expects a POST request with JSON data containing the field "barcode".
    Returns location details as JSON if found.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            barcode = data.get('barcode')
            if barcode:
                try:
                    location_obj = Location.objects.get(location_id=barcode)
                    location_data = {
                        'location_id': location_obj.location_id,
                        'warehouse_id': location_obj.warehouse_id,
                        'location_type': location_obj.location_type,
                        'status': location_obj.status,
                        #'item_restrictions': location_obj.item_restrictions,
                        #'date_created': location_obj.date_created.isoformat(),
                        #'date_modified': location_obj.date_modified.isoformat(),
                        'success': True,
                    }
                    return JsonResponse(location_data)
                except Location.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Location not found'})
            else:
                return JsonResponse({'success': False, 'message': 'No barcode provided'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def get_inventory_by_whseSKU(whseSKU):
    try:
        product = Product.objects.get(whseSKU=whseSKU)
        inventory_item = Inventory.objects.filter(product=product).first()
        return inventory_item
    except Product.DoesNotExist:
        return Inventory.objects.none()
   

@csrf_exempt
@login_required
def record_movement(request):
    """
    Expects a POST request with JSON data.
    Supports recording one or multiple movement records.
    Converts passed location and container identifiers to model instances.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Determine who moved the item(s)
            moved_by_id = data.get('moved_by')
            if moved_by_id:
                try:
                    moved_by = User.objects.get(id=moved_by_id)
                except User.DoesNotExist:
                    moved_by = request.user
            else:
                moved_by = request.user
            print(moved_by,data)
            movement_reason = data.get('movement_reason')
            from_location_id = data.get('from_location')
            to_location_id = data.get('to_location')
            from_container_barcode = data.get('from_container')
            to_container_barcode = data.get('to_container')

            from_location_obj = None
            to_location_obj = None
            from_container_obj = None
            to_container_obj = None

            if from_location_id:
                try:
                    from_location_obj = Location.objects.get(location_id=from_location_id)
                except Location.DoesNotExist:
                    from_location_obj = None

            if to_location_id:
                try:
                    to_location_obj = Location.objects.get(location_id=to_location_id)
                except Location.DoesNotExist:
                    to_location_obj = None

            if from_container_barcode:
                try:
                    from_container_obj = Container.objects.get(barcode=from_container_barcode)
                except Container.DoesNotExist:
                    from_container_obj = None

            if to_container_barcode:
                try:
                    to_container_obj = Container.objects.get(barcode=to_container_barcode)
                except Container.DoesNotExist:
                    to_container_obj = None

            movements = data.get('movements')
            print(movements,"these moves")
            if movements and isinstance(movements, list):
                for movement_item in movements:
                    item_barcode = movement_item.get('item_barcode')
                    event_time = datetime.fromisoformat(movement_item.get('eventTime'))
                    print(event_time," is the TIME")
                    try:
                        inventory_item = get_inventory_by_whseSKU(item_barcode)
                        print(inventory_item)
                        print(f'item does exist {inventory_item.barcode}')    
                    except Inventory.DoesNotExist:
                        inventory_item=item_barcode
                        print(f'item does not exist {inventory_item}')
                        #continue  # or return an error response if preferred
                    MovementHistory.objects.create(
                        inventory_item=inventory_item,
                        from_location=from_location_obj,
                        to_location=to_location_obj,
                        from_container=from_container_obj,
                        to_container=to_container_obj,
                        movement_reason=movement_reason,
                        moved_by=moved_by,
                        event_time=event_time  # provided by client
                    )
                return JsonResponse({'message': 'Movements recorded successfully'}, status=201)
            else:
                # Fallback: single movement record.
                item_barcode = data.get('item_barcode')
                try:
                    inventory_item = Inventory.objects.get(whseSKU=item_barcode)
                except Inventory.DoesNotExist:
                    return JsonResponse({'error': 'Inventory item not found'}, status=400)
                MovementHistory.objects.create(
                    inventory_item=inventory_item,
                    from_location=from_location_obj,
                    to_location=to_location_obj,
                    from_container=from_container_obj,
                    to_container=to_container_obj,
                    movement_reason=movement_reason,
                    moved_by=moved_by,
                )
                return JsonResponse({'message': 'Movement recorded successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'warehouse/location_list.html', {'locations': locations})

# Containers
@login_required
@permission_required('warehouse.add_container', raise_exception=True)
def create_container(request):
    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('container-list')
    else:
        form = ContainerForm()
    return render(request, 'warehouse/create_container.html', {'form': form})

@login_required
def container_list(request):
    containers = Container.objects.all()
    return render(request, 'warehouse/container_list.html', {'containers': containers})

def dashboard(request):
    pass
