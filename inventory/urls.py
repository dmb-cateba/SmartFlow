from django.urls import path
from inventory import views

urlpatterns = [
    path('', views.index, name='index'),
    path('metrics/', views.inventory_metrics, name='inventory_metrics'),
]