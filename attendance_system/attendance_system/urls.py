# attendance_system/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('attendance/', include('attendance.urls')),  # Inchlude attendance URLs
]
