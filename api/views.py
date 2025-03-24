from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from django.shortcuts import get_object_or_404
from warehouse.models import Location, Container, Inventory, MovementHistory
from .serializers import (
    LocationSerializer,
    ContainerSerializer,
    InventorySerializer,
    MovementHistorySerializer,
)
 
class ScanReceiveInventoryAPIView(APIView):
    """
    When a barcode is scanned, try to resolve it as a container first;
    if not found, check if it’s a location. Returns the details along with
    aggregated information (e.g., item counts).
    """
    def post(self, request, format=None):
        barcode = request.data.get('barcode')
        if not barcode:
            return Response({"error": "Barcode is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Attempt to fetch as Container
        try:
            container = Container.objects.get(barcode=barcode)
            serializer = ContainerSerializer(container)
            data = serializer.data
            # Aggregate inventory items in the container
            total_items = Inventory.objects.filter(container=container).aggregate(total=models.Sum('quantity'))
            data['total_items'] = total_items.get('total', 0)
            return Response(data, status=status.HTTP_200_OK)
        except Container.DoesNotExist:
            # Attempt to fetch as Location
            try:
                location = Location.objects.get(location_id=barcode)
                serializer = LocationSerializer(location)
                # Retrieve containers in this location (if applicable)
                containers = Container.objects.filter(current_location=location)
                container_serializer = ContainerSerializer(containers, many=True)
                data = serializer.data
                data['containers'] = container_serializer.data
                return Response(data, status=status.HTTP_200_OK)
            except Location.DoesNotExist:
                return Response({"error": "Barcode does not match any container or location."}, status=status.HTTP_404_NOT_FOUND)

class MoveInventoryAPIView(APIView):
    """
    Moves inventory from one location to another, recording the movement.
    Expects item barcode, from_location, to_location, and quantity.
    """
    def post(self, request, format=None):
        item_barcode = request.data.get('item_barcode')
        from_location_id = request.data.get('from_location')
        to_location_id = request.data.get('to_location')
        quantity = request.data.get('quantity')
        
        if not all([item_barcode, from_location_id, to_location_id]):
            return Response({"error": "item_barcode, from_location, and to_location are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate and retrieve the inventory item
        inventory = get_object_or_404(Inventory, barcode=item_barcode)
        
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({"error": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve locations (you might add further validations here)
        from_location = get_object_or_404(Location, location_id=from_location_id)
        to_location = get_object_or_404(Location, location_id=to_location_id)
        
        # Record the movement (additional business logic can be added here)
        movement = MovementHistory.objects.create(
            item_barcode=item_barcode,
            from_location=from_location_id,
            to_location=to_location_id,
            movement_reason="MOVE_INVENTORY",  # Adjust as needed
            moved_by=request.user
        )
        serializer = MovementHistorySerializer(movement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateLocationAPIView(APIView):
    """
    Allows updating location details, such as status or priority.
    """
    def post(self, request, format=None):
        location_id = request.data.get('location_id')
        if not location_id:
            return Response({"error": "location_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        location = get_object_or_404(Location, location_id=location_id)
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PalletManagementAPIView(APIView):
    """
    Handles creation and closure of pallets.
    - POST to create a new pallet (Container with type 'PALLET').
    - PUT to close a pallet (e.g., mark it as 'CLOSED').
    """
    def post(self, request, format=None):
        barcode = request.data.get('barcode')
        location_id = request.data.get('location_id')
        if not all([barcode, location_id]):
            return Response({"error": "barcode and location_id are required."}, status=status.HTTP_400_BAD_REQUEST)
        location = get_object_or_404(Location, location_id=location_id)
        pallet = Container.objects.create(
            barcode=barcode,
            container_type='PALLET',
            current_location=location,
            status='ACTIVE'
        )
        serializer = ContainerSerializer(pallet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, format=None):
        barcode = request.data.get('barcode')
        if not barcode:
            return Response({"error": "barcode is required."}, status=status.HTTP_400_BAD_REQUEST)
        pallet = get_object_or_404(Container, barcode=barcode, container_type='PALLET')
        pallet.status = 'CLOSED'  # Adjust status to indicate pallet closure
        pallet.save()
        serializer = ContainerSerializer(pallet)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoadPalletToTruckAPIView(APIView):
    """
    Marks a pallet as loaded onto a truck.
    """
    def post(self, request, format=None):
        barcode = request.data.get('barcode')
        if not barcode:
            return Response({"error": "barcode is required."}, status=status.HTTP_400_BAD_REQUEST)
        pallet = get_object_or_404(Container, barcode=barcode, container_type='PALLET')
        # Update the pallet’s status to reflect that it has been loaded
        pallet.status = 'LOADED'
        pallet.save()
        serializer = ContainerSerializer(pallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
