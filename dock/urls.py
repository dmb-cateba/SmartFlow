from django.urls import path
from .views import dock_view

urlpatterns = [
    path('', dock_view, name='dock_view'),
]