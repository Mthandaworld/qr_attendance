# attendance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('check-in/', views.check_in_page, name='check_in_page'),
    path('process-check-in/', views.process_check_in, name='process_check_in'),
    path('attendance_logs/', views.attendance_logs, name='attendance_logs'), 
    # urls.py
    path('export_logs_csv/', views.export_logs_csv, name='export_logs_csv'),

]

