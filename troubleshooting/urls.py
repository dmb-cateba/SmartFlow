from django.urls import path
from troubleshooting import views

urlpatterns = [
    path('', views.index, name='index'),
]