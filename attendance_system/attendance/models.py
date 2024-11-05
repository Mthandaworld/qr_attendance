from django.db import models

# Create your models here.


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    parent_email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class AttendanceLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} checked in at{self.check_in_time}"
