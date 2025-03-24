from django.urls import path
from load_tracker import views

urlpatterns = [
    path('', views.index, name='index'),
]