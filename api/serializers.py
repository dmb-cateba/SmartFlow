from rest_framework import serializers
from warehouse.models import Location, Container, Inventory, MovementHistory, InventoryAdjustment

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class MovementHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementHistory
        fields = '__all__'

class InventoryAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAdjustment
        fields = '__all__'
