from django.contrib import admin
from .models import Student, AttendanceLog

# Register your models here.

admin.site.register(Student)
admin.site.register(AttendanceLog)