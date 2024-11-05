# attendance/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Student, AttendanceLog
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.db.models import Q
import csv
from django.http import HttpResponse


def check_in_page(request):
    return render(request, 'attendance/check_in.html')


def process_check_in(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')

        #check if studentID is received
        print("Received students_id:", student_id)
        
        # Lookup the student by their ID
        try:
            student = Student.objects.get(student_id=student_id)
            
            # Log the attendance with the current time
            AttendanceLog.objects.create(student=student, check_in_time=timezone.now())

            #Try sending email to parent
            send_mail(
                subject="Student Check-In Notification",
                message=f"Dear Parent, your child{student.name} has checked in successfully.",
                from_email='mthandazomoyo75@gmail.com',
                recipient_list=[student.parent_email],
                fail_silently=False,
            )


            #redirect back to checkin page with a success message

            return render(request, "attendance/check_in.html",{'message':f"Checkin successful for {student.name}"})
        
        except Student.DoesNotExist:
            return render(request, "attendance/check_in.html", {'error': "Student not found. Please try again."})
    
    return redirect('check_in_page')


def attendance_logs(request):
    query = request.GET.get('query', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    logs = AttendanceLog.objects.select_related('student').all().order_by('-check_in_time')

    # Apply search and date filtering
    if query:
        logs = logs.filter(Q(student__student_id__icontains=query) | Q(student__name__icontains=query))
    if start_date:
        logs = logs.filter(check_in_time__date__gte=parse_date(start_date))
    if end_date:
        logs = logs.filter(check_in_time__date__lte=parse_date(end_date))

    return render(request, 'attendance/attendance_logs.html', {
        'logs': logs,
        'query': query,
        'start_date': start_date,
        'end_date': end_date
    })

    logs = logs.order_by('-check_in_time')  # Order logs

    # Paginate logs
    paginator = Paginator(logs, 10)  # Show 10 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'attendance/attendance_logs.html', {
        'page_obj': page_obj,  # Send paginated page object
        'query': query,
        'start_date': start_date,
        'end_date': end_date
    })

def export_logs_csv(request):
    logs = AttendanceLog.objects.select_related('student').all().order_by('-check_in_time')

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Name', 'Check-In Time'])

    for log in logs:
        writer.writerow([log.student.student_id, log.student.name, log.check_in_time])

    return response