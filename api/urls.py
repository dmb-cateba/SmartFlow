from django.urls import path
from .views import (
    ScanReceiveInventoryAPIView,
    MoveInventoryAPIView,
    UpdateLocationAPIView,
    PalletManagementAPIView,
    LoadPalletToTruckAPIView
)

urlpatterns = [
    path('scan/receive/', ScanReceiveInventoryAPIView.as_view(), name='scan-receive-inventory'),
    path('move-inventory/', MoveInventoryAPIView.as_view(), name='move-inventory'),
    path('update-location/', UpdateLocationAPIView.as_view(), name='update-location'),
    path('pallet/', PalletManagementAPIView.as_view(), name='pallet-management'),
    path('pallet/load/', LoadPalletToTruckAPIView.as_view(), name='load-pallet'),
]