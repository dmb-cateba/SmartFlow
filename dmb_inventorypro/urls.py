# project urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('warehouse/', include(('warehouse.urls', 'warehouse'), namespace='warehouse')),
    path('dock/', include(('dock.urls', 'dock'), namespace='dock')),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('load_tracker/', include(('load_tracker.urls', 'load_tracker'), namespace='load_tracker')),
    path('work_plans/', include(('work_plans.urls', 'work_plans'), namespace='work_plans')),
    path('troubleshooting/', include(('troubleshooting.urls', 'troubleshooting'), namespace='troubleshooting')),
]
