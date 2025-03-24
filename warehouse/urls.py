from django.urls import path
from . import views

urlpatterns = [
    path('scanner/', views.scanner_view, name='scanner'),
    path('locations/', views.location_list, name='location-list'),
    path('location_detail/', views.location_detail, name='location_detail'),
    path('locations/create/', views.create_location, name='create-location'),
    path('containers/', views.container_list, name='container-list'),
    path('containers/create/', views.create_container, name='create-container'),
    path('record_movement/', views.record_movement, name='record_movement'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
