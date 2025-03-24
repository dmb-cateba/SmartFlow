from django.urls import path
from work_plans import views

urlpatterns = [
    path('', views.index, name='index'),
]